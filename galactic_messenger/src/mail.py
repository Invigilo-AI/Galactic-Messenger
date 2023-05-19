from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import TypedDict, Union, cast

import aiosmtplib

from config import Config


class SMTPUrl(TypedDict):
    zoho: str
    gmail: str


class SMTPPort(TypedDict):
    gmail: int
    zoho: int


smtp_url: SMTPUrl = {"zoho": "smtp.zoho.com", "gmail": "smtp.gmail.com"}
smtp_port: SMTPPort = {"zoho": 587, "gmail": 587}


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


async def _create_server_connection(
    url: str, port: int, mail: str, password: str
) -> aiosmtplib.SMTP:
    server = aiosmtplib.SMTP(url, port)
    await server.connect()
    await server.login(mail, password)
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


async def _send(server: aiosmtplib.SMTP, body: MIMEMultipart) -> bool:
    async with server:
        return True if await server.send_message(body) else False


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


def setup_email(mail: str, password: str):
    async def send_email(email_content: EmailContent) -> bool:
        server = await _create_server_connection(
            smtp_url[Config.SMTP_SERVER.lower()],
            smtp_port[Config.SMTP_SERVER.lower()],
            mail,
            password,
        )
        email_body = _create_email_body(mail, email_content)

        success = await _send(server, email_body)
        return success

    return send_email
