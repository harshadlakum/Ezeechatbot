import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm

OUTPUT_PATH = os.path.join("sample_data", "acme_hr_policy.pdf")
os.makedirs("sample_data", exist_ok=True)

CONTENT = [
    ("Acme Corp - HR Policy and Employee Support Guide", "h1"),
    ("This document outlines the official HR policies and employee support procedures at Acme Corp.", "body"),
    ("1. Leave Policy", "h2"),
    ("Employees are entitled to 18 days of paid annual leave per calendar year. Casual leave is limited to 6 days per year and cannot be carried forward. Sick leave is 12 days per year with a valid medical certificate required for more than 2 consecutive days. Maternity leave is 26 weeks. Paternity leave is 5 working days. All leave requests must be submitted via the HR portal at least 3 days in advance.", "body"),
    ("2. Work From Home Policy", "h2"),
    ("Employees may work from home up to 2 days per week subject to manager approval. Full-time remote work is not permitted unless explicitly approved by the department head and HR. Employees must be available during core hours 10 AM to 5 PM IST.", "body"),
    ("3. Reimbursement Policy", "h2"),
    ("Local travel reimbursements are capped at INR 2,000 per day. Outstation travel is reimbursed at actuals up to INR 10,000 per day for hotels. Meal reimbursements are capped at INR 800 per day. All reimbursements must be claimed within 30 days.", "body"),
    ("4. Payroll and Salary Cycle", "h2"),
    ("Salaries are processed on the last working day of every month. Salary slips are available on the employee self-service portal by the 1st of the following month. Salary discrepancies must be reported to HR within 7 days.", "body"),
    ("5. Laptop and IT Support", "h2"),
    ("Each employee is issued a company laptop within 3 working days of joining. If your laptop crashes raise a ticket on the IT helpdesk portal or email it-support@acmecorp.com. A replacement is provided within 2 working days for critical issues.", "body"),
    ("6. Office Timings", "h2"),
    ("Standard office hours are 9:30 AM to 6:30 PM IST Monday to Friday. Core hours are 10 AM to 5 PM. Flexible start times between 8 AM and 10 AM are permitted with manager approval.", "body"),
]

styles = getSampleStyleSheet()
story = []
for text, style_key in CONTENT:
    if style_key == "h1":
        p = Paragraph(f"<b><font size=16>{text}</font></b>", styles["Heading1"])
    elif style_key == "h2":
        p = Paragraph(f"<b>{text}</b>", styles["Heading2"])
    else:
        p = Paragraph(text, styles["BodyText"])
    story.append(p)
    story.append(Spacer(1, 0.3 * cm))

doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=A4)
doc.build(story)
print(f"Sample PDF created: {OUTPUT_PATH}")
