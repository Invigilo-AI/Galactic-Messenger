from enum import Enum
import requests


class Service(Enum):
    WHATSAPP = "WHATSAPP"
    TELEGRAM = "TELEGRAM"
    EMAIL = "EMAIL"


class Alert:
    def __init__(self, service, token, secret):
        if service == Service.WHATSAPP:
            self = WhatsappAlert(service, token, secret)


class WhatsappAlert(Alert):
    def __init__(self, service, token, secret):
        return

    def send_message(self, message: str):
        return

    def send_image(self, message: str, image_bytes: bytes):
        return

    def send_video(self, message: str, video_bytes: bytes):
        return


class TelegramAlert(Alert):
    def __init__(self, service, token, secret):
        return

    def send_message(self, message: str):
        return

    def send_image(self, message: str, image_bytes: bytes):
        return

    def send_video(self, message: str, video_bytes: bytes):
        return


class EmailAlert(Alert):
    def __init__(self, service, token, secret):
        return

    def send_message(self, message: str):
        return

    def send_image(self, message: str, image_bytes: bytes):
        return

    def send_video(self, message: str, video_bytes: bytes):
        return
