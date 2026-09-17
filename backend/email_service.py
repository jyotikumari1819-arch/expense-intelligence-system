"""
Sends password-reset emails via SMTP if configured; otherwise falls back to
printing the reset link straight to the backend console, so the whole flow
works locally with zero email setup.
"""
import smtplib
from email.mime.text import MIMEText
from config import settings

FRONTEND_RESET_URL = "http://localhost:5173/reset-password"


def send_password_reset_email(to_email: str, token: str) -> None:
    reset_link = f"{FRONTEND_RESET_URL}?token={token}"

    if not settings.smtp_host or not settings.smtp_user or not settings.smtp_password:
        print("\n" + "=" * 60)
        print(f"[DEV MODE] No SMTP configured — password reset link for {to_email}:")
        print(reset_link)
        print("=" * 60 + "\n")
        return

    msg = MIMEText(
        f"Hi,\n\nYou requested a password reset for Expense Intelligence System.\n"
        f"Click the link below to set a new password (valid for 30 minutes):\n\n"
        f"{reset_link}\n\n"
        f"If you didn't request this, you can safely ignore this email."
    )
    msg["Subject"] = "Reset your password — Expense Intelligence System"
    msg["From"] = settings.smtp_user
    msg["To"] = to_email

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
    except Exception as e:
        # Don't let email failures crash the request — fall back to console
        # so the person testing locally can still complete the flow.
        print(f"[WARN] Failed to send reset email ({e}). Falling back to console link:")
        print(reset_link)
