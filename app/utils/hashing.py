import uuid


def generate_bot_id() -> str:
    return str(uuid.uuid4())
