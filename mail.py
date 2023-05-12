import smtplib
from config import Config
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from typing import cast, TypedDict, Callable, Union


class PlainEmailContent(TypedDict):
    to: str
    subject: str
    message: str


class WithAttachmentEmailContent(TypedDict):
    to: str
    subject: str
    message: str
    attachment_name: str
    attachment: bytes


EmailContent = Union[PlainEmailContent, WithAttachmentEmailContent]


def _create_server_connection(
    url: str, port: int, mail: str, password: str
) -> smtplib.SMTP:
    server = smtplib.SMTP(url, port)
    server.starttls()
    server.login(mail, password)
    return server


def _create_email_plain_body(
    send_from: str, send_to: str, subject: str, message: str
) -> MIMEMultipart:
    email_body = MIMEMultipart()
    email_body["From"] = send_from
    email_body["To"] = send_to
    email_body["Subject"] = subject
    email_body.attach(MIMEText(message, "plain"))
    return email_body


def _create_email_with_attachment_body(
    send_from: str,
    send_to: str,
    subject: str,
    message: str,
    attachment_name: str,
    attachment: bytes,
) -> MIMEMultipart:
    email_body = _create_email_plain_body(send_from, send_to, subject, message)
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment)
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition", f"attachment; filename={attachment_name}"
    )
    email_body.attach(part)
    return email_body


def _send(server: smtplib.SMTP, body: MIMEMultipart) -> bool:
    server.send_message(body)
    return True


def _close_server_connection(server: smtplib.SMTP) -> None:
    server.quit()


def _create_email_body(
    mail: str, email_content: EmailContent
) -> MIMEMultipart:
    if "attachment_name" in email_content and "attachment" in email_content:
        email_content_typed = cast(WithAttachmentEmailContent, email_content)
        return _create_email_with_attachment_body(
            mail,
            email_content_typed["to"],
            email_content_typed["subject"],
            email_content_typed["message"],
            email_content_typed["attachment_name"],
            email_content_typed["attachment"],
        )
    else:
        email_content_typed = cast(PlainEmailContent, email_content)
        return _create_email_plain_body(
            mail,
            email_content_typed["to"],
            email_content_typed["subject"],
            email_content_typed["message"],
        )


def set_email(mail: str, password: str) -> Callable[[EmailContent], bool]:
    def send_email(email_content: EmailContent) -> bool:
        server = _create_server_connection(
            Config.SMTP_SERVER, Config.SMTP_PORT, mail, password
        )
        email_body = _create_email_body(mail, email_content)

        success = _send(server, email_body)
        _close_server_connection(server)
        return success

    return send_email
