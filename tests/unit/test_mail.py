import smtplib
from unittest.mock import MagicMock, Mock

from galactic_messenger.src.mail import (_create_email_body,
                                         _create_email_plain_body,
                                         _create_email_with_attachment_body,
                                         _create_server_connection, _send,
                                         setup_email)


def test_send_email():
    smtplib.SMTP = MagicMock(return_value=MagicMock())
    server = smtplib.SMTP()
    server.starttls.return_value = None
    server.login.return_value = None
    server.send_message.return_value = None

    send_email = setup_email("example@invigilo.sg", "example_password")
    assert (
        send_email(
            {
                "to": "example@gmail.com",
                "subject": "example subject",
                "message": "example message",
                "attachment_name": "file",
                "attachment": open("tests/data/SampleImage.jpg", "rb").read(),
            }
        )
        is True
    )


def test_create_server_connection():
    url = "smtp.example.com"
    port = 587
    mail = "test@example.com"
    password = "password"

    server = _create_server_connection(url, port, mail, password)

    assert server


def test_create_email_plain_body():
    send_from = "test@example.com"
    send_to = "recipient@example.com"
    subject = "Test Email"
    message = "Hello, World!"

    email_body = _create_email_plain_body(send_from, send_to, subject, message)

    assert email_body["From"] == send_from
    assert email_body["To"] == send_to
    assert email_body["Subject"] == subject
    assert len(email_body.get_payload()) == 1
    assert email_body.get_payload()[0].get_content_type() == "text/plain"
    assert email_body.get_payload()[0].get_payload() == message


def test_create_email_with_attachment_body():
    send_from = "test@example.com"
    send_to = "recipient@example.com"
    subject = "Test Email"
    message = "Hello, World!"
    attachment_name = "example.txt"
    attachment = b"Example Attachment"

    email_body = _create_email_with_attachment_body(
        send_from, send_to, subject, message, attachment_name, attachment
    )

    assert email_body["From"] == send_from
    assert email_body["To"] == send_to
    assert email_body["Subject"] == subject
    assert len(email_body.get_payload()) == 2
    assert email_body.get_payload()[0].get_content_type() == "text/plain"
    assert email_body.get_payload()[0].get_payload() == message
    assert (
        email_body.get_payload()[1].get_content_type()
        == "application/octet-stream"
    )
    assert (
        email_body.get_payload()[1]["Content-Disposition"]
        == f"attachment; filename={attachment_name}"
    )


def test_send():
    server = Mock()
    body = Mock()

    assert _send(server, body)
    server.send_message.assert_called_once_with(body)


def test_create_email_body():
    mail = "test@example.com"
    plain_email_body = _create_email_body(
        mail,
        {
            "to": "recipient@example.com",
            "subject": "Test Email",
            "message": "Hello, World!",
        },
    )
    attachment_email_body = _create_email_body(
        mail,
        {
            "to": "recipient@example.com",
            "subject": "Test Email",
            "message": "Hello, World!",
            "attachment_name": "example.txt",
            "attachment": b"Example Attachment",
        },
    )

    assert plain_email_body.get_payload()[0].get_content_type() == "text/plain"
    assert (
        attachment_email_body.get_payload()[0].get_content_type()
        == "text/plain"
    )
