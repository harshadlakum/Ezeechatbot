# EzeeChatBot — RAG Chatbot API

A production-style RAG (Retrieval-Augmented Generation) backend API that allows users to upload any knowledge base — PDF, URL, or raw text — and instantly get a chatbot that answers questions grounded only in that content.

Built as Task E-1 of the AI Engineer assessment.

---

## What It Does

- Accepts PDF files, URLs, or raw text as knowledge base input
- Chunks content using sentence-aware splitting with overlap
- Generates embeddings using a local sentence-transformer model
- Stores vectors in Qdrant with full bot isolation per upload
- Answers questions using a local LLM via Ollama
- Refuses to answer questions outside the uploaded content
- Tracks per-bot stats: messages served, latency, cost, unanswered count

---

## Tech Stack

Component      Technology                        
API Framework  FastAPI + Uvicorn                 
Embeddings     sentence-transformers (all-MiniLM-L6-v2) 
Vector DB      Qdrant (local persistent mode)    
LLM            Ollama (qwen2.5:3b)               
Database       SQLite via SQLAlchemy async       
PDF Parsing    PyMuPDF                           
URL Parsing    httpx + BeautifulSoup4            
Validation     Pydantic v2                       
Testing        pytest + pytest-asyncio           

---

## Local Setup

### Prerequisites
- Python 3.11
- Ollama installed from https://ollama.com/download

### Steps

\\\ash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ezeechatbot.git
cd ezeechatbot

# Create and activate virtual environment
python -m venv venv
venv\Scripts\Activate.ps1        # Windows
source venv/bin/activate          # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env

# Pull the LLM model
ollama pull qwen2.5:3b

# Generate sample PDF for testing
python scripts/create_sample_pdf.py

# Start the API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
\\\

Swagger UI: http://127.0.0.1:8080/docs

---

## Environment Variables

See .env.example for all configurable values.

 Variable                    Default              Description                        
 OLLAMA_MODEL               qwen2.5:3b            Local LLM model name               
 EMBEDDING_MODEL            all-MiniLM-L6-v2      Sentence transformer model         
 QDRANT_PATH                ./data/qdrant_storage Local vector storage path          
 CHUNK_SIZE                 512                   Max characters per chunk           
 CHUNK_OVERLAP              64                    Overlap between consecutive chunks 
 RELEVANCE_SCORE_THRESHOLD  0.35                  Minimum cosine score to use chunk  
 RETRIEVAL_TOP_K            5                     Number of chunks retrieved         

---

## API Endpoints

Method  Endpoint                   Description                     
GET     /api/v1/health             Health check                    
POST    /api/v1/upload             Upload text, URL, or PDF        
POST    /api/v1/chat               Chat with an uploaded bot       
GET     /api/v1/stats/{bot_id}     Get usage stats for a bot       

---

## Testing the API

### 1. Upload raw text

\\\ash
curl -X POST "http://127.0.0.1:8080/api/v1/upload" \
  -F "source_type=text" \
  -F "text=Employees get 18 days annual leave and 6 days casual leave per year."
\\\

### 2. Upload a URL

\\\ash
curl -X POST "http://127.0.0.1:8080/api/v1/upload" \
  -F "source_type=url" \
  -F "url=https://en.wikipedia.org/wiki/Python_(programming_language)"
\\\

### 3. Upload a PDF

\\\ash
curl -X POST "http://127.0.0.1:8080/api/v1/upload" \
  -F "source_type=pdf" \
  -F "file=@sample_data/acme_hr_policy.pdf;type=application/pdf"
\\\

### 4. Chat with a bot

\\\ash
curl -X POST "http://127.0.0.1:8080/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "YOUR_BOT_ID",
    "user_message": "How many casual leaves do employees get?",
    "conversation_history": []
  }'
\\\

### 5. Get stats

\\\ash
curl "http://127.0.0.1:8080/api/v1/stats/YOUR_BOT_ID"
\\\

---

## Run Tests

\\\ash
pytest tests/ -v
\\\

---

## Chunking Strategy

Text is split using a sentence-aware recursive chunker:

1. Text is first split at sentence boundaries using punctuation endings
2. Sentences are accumulated into chunks up to CHUNK_SIZE characters
3. When a chunk is full, the last CHUNK_OVERLAP characters carry into the next chunk
4. Each chunk stores metadata: bot_id, source_type, chunk_index, char_count

Why not naive character splitting: splitting mid-sentence destroys semantic meaning and directly hurts retrieval quality. Sentence-aware splitting ensures each chunk is a coherent unit of information.

---

## No-Answer Fallback

The system has two layers of hallucination prevention:

1. If vector search returns no chunks above the relevance threshold, the fallback message is returned immediately without calling the LLM
2. If the LLM responds with known uncertainty phrases, was_answered is set to false and unanswered_questions is incremented in stats

The system prompt explicitly instructs the LLM to respond only from the provided context and to use a specific fallback phrase if the answer is not found.

---

## Stats Tracking

All stats are stored per message in SQLite:

Field                         How it is calculated                            
total_messages_served        COUNT of all messages for this bot              
verage_response_latency_ms   AVG of latency_ms across all messages         
estimated_token_cost_usd     SUM of cost_usd (0.0 for local Ollama)          
unanswered_questions         COUNT of messages where was_answered = false    

---

## Bot Isolation

Every upload creates a unique bot_id (UUID4). All Qdrant vectors are stored with bot_id as a payload field. All searches use a Qdrant filter to query only that bot's vectors. One bot cannot access another bot's content under any circumstance.

---

## Assumptions

- Ollama must be running locally before starting the API
- Token cost is 0.0 for local Ollama by default. Update COST_PER_1K_INPUT_TOKENS and COST_PER_1K_OUTPUT_TOKENS in .env for cloud LLM pricing
- Qdrant runs in local file mode with no external dependency
- The data/ folder is excluded from Git and is created automatically on first run
