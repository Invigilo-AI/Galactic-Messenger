import smtplib
from unittest.mock import MagicMock
from mail import set_email
from utils import compose


def test_compose():
    def add_7(x):
        return x + 7

    def mul_13(x):
        return x * 13

    add_7_and_mul_13 = compose(add_7, mul_13)

    assert add_7_and_mul_13(9) is add_7(mul_13(9))


def test_send_email():
    smtplib.SMTP = MagicMock(return_value=MagicMock())
    server = smtplib.SMTP()
    server.starttls.return_value = None
    server.login.return_value = None
    server.send_message.return_value = None

    send_email = set_email("example@invigilo.sg", "example_password")
    assert send_email("example@gmail.com", "example", "example body") is True
