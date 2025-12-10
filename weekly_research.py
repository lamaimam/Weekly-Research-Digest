import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# --- Feeds you want to track ---
FEEDS = {
    "AI": "https://export.arxiv.org/rss/cs.AI",
    "Robotics": "https://export.arxiv.org/rss/cs.RO",
    "Quantum Physics": "https://export.arxiv.org/rss/quant-ph",
    "Physics": "https://export.arxiv.org/rss/physics.gen-ph",
}

# --- Email config ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "lalturki20@gmail.com"
PASSWORD = "mvkibttydazdoenb"   # Use Gmail App Password, not your main password
TO_EMAIL = "lalturki20@gmail.com"

# --- Collect papers ---
def get_papers():
    papers = []
    for topic, url in FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:  # latest 10 per topic
            papers.append(f"<b>[{topic}]</b> {entry.title}<br>{entry.link}<br><br>")
    return papers

# --- Send email ---
def send_email(content):
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = f"Weekly Research Digest - {datetime.now().strftime('%Y-%m-%d')}"

    body = MIMEText("<br>".join(content), "html")
    msg.attach(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, TO_EMAIL, msg.as_string())

if __name__ == "__main__":
    papers = get_papers()
    if papers:
        send_email(papers)
