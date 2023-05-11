import smtplib
from typing import NamedTuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

Config = NamedTuple("Config", [("SMTP_SERVER", str), ("SMTP_PORT", int)])(
    "smtp.zoho.com", 587
)


def _create_server_connection(
    url: str, port: int, mail: str, password: str
) -> smtplib.SMTP:
    server = smtplib.SMTP(url, port)
    server.starttls()
    server.login(mail, password)
    return server


def _create_email_body(
    send_from: str, send_to: str, subject: str, message: str
) -> MIMEMultipart:
    email_body = MIMEMultipart()
    email_body["From"] = send_from
    email_body["To"] = send_to
    email_body["Subject"] = subject
    email_body.attach(MIMEText(message, "plain"))
    return email_body


def _send(server: smtplib.SMTP, body: MIMEMultipart) -> bool:
    server.send_message(body)
    return True


def _close_server_connection(server: smtplib.SMTP) -> None:
    server.quit()


def set_email(mail: str, password: str):
    def send_email(to: str, subject: str, message: str):
        server = _create_server_connection(
            Config.SMTP_SERVER, Config.SMTP_PORT, mail, password
        )
        email_body = _create_email_body(mail, to, subject, message)
        success = _send(server, email_body)
        _close_server_connection(server)
        return success

    return send_email


send_email = set_email("anonone@zohomail.com", "anon13579")
send_email("mail2anonone@gmail.com", "hello", "hi, this is my first email")
