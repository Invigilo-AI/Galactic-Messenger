import smtplib
from unittest.mock import MagicMock
from mail import set_email


def test_send_email():
    smtplib.SMTP = MagicMock(return_value=MagicMock())
    server = smtplib.SMTP()
    server.starttls.return_value = None
    server.login.return_value = None
    server.send_message.return_value = None

    send_email = set_email("example@invigilo.sg", "example_password")
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
