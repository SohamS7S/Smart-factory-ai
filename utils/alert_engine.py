import os
import smtplib
from email.message import EmailMessage
import pyttsx3
from dotenv import load_dotenv
load_dotenv()

def send_email(subject, body):
    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_PASS")
    receiver = os.getenv("RECEIVER_EMAIL")

    if not sender or not password or not receiver:
        print("⚠️ Email credentials not set properly in .env")
        return

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print("❌ Email failed:", e)

def send_alert(title, message):
    if os.getenv("EMAIL_ALERTS", "on") == "on":
        send_email(subject=title, body=message)

    if os.getenv("VOICE_ALERTS", "on") == "on":
        print("🔊 Voice Alert:", message)
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()

    if os.getenv("CONSOLE_ALERTS", "on") == "on":
        print(f"📣 {title}: {message}")
