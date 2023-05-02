from typing import TypedDict, Literal
from enum import Enum
import json
import aiohttp


class Config(Enum):
    SINGLE_CONNECT_TIMEOUT = 5
    BATCH_CONNECT_TIMEOUT = 5
    SINGLE_TOTAL_TIMEOUT = 10
    BATCH_TOTAL_TIMEOUT = 60


class Service(Enum):
    WHATSAPP = "WHATSAPP"
    TELEGRAM = "TELEGRAM"
    EMAIL = "EMAIL"


ServiceInput = Literal["WHATSAPP", "TELEGRAM", "EMAIL"]


class MessagePayload(TypedDict):
    message: str


class Alert:
    def __init__(self, service: ServiceInput, token: str, chatId: str) -> None:
        if service == Service.WHATSAPP:
            self.client = WhatsappAlert(token, chatId)
        elif service == Service.TELEGRAM:
            self.client = TelegramAlert(token, chatId)
        elif service == Service.EMAIL:
            self.client = EmailAlert(token, chatId)
        else:
            raise Exception("Input Service is Invalid!")

    def send_one_message(self, message: str):
        return self.client.send_one_message(message)

    def send_one_image(self, message: str, image_bytes: bytes):
        return self.client.send_one_image(message, image_bytes)

    def send_one_video(self, message: str, video_bytes: bytes):
        return self.client.send_one_video(message, video_bytes)


class WhatsappMessagePayload(MessagePayload):
    groupId: str


class WhatsappAlert:
    def __init__(self, ip: str, groupId: str):
        self.url = f"http://{ip}:5000/sendWhatsapp"
        self.groupId = groupId

    async def send_one_message(self, message: str):
        payload: WhatsappMessagePayload = {
            "groupId": self.groupId,
            "message": message,
        }
        timeout_options = aiohttp.ClientTimeout(
            total=Config.SINGLE_TOTAL_TIMEOUT.value
        )
        client = aiohttp.ClientSession(timeout=timeout_options)
        response = await client.post(
            self.url + "/message", json=json.dumps(payload)
        )
        response_json = await response.json()
        await client.close()
        return response_json

    def send_one_image(self, message: str, image_bytes: bytes):
        return

    def send_one_video(self, message: str, video_bytes: bytes):
        return


class TelegramAlert:
    def __init__(self, token, secret):
        return

    def send_one_message(self, message: str):
        return

    def send_one_image(self, message: str, image_bytes: bytes):
        return

    def send_one_video(self, message: str, video_bytes: bytes):
        return


class EmailAlert:
    def __init__(self, token, secret):
        return

    def send_one_message(self, message: str):
        return

    def send_one_image(self, message: str, image_bytes: bytes):
        return

    def send_one_video(self, message: str, video_bytes: bytes):
        return
