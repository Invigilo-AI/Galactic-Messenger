from typing import TypedDict, Literal, Union
from enum import Enum
import aiohttp
import base64
import json


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


class ImagePayload(TypedDict):
    message: str
    image_bytes: bytes


class VideoPayload(TypedDict):
    message: str
    video_bytes: bytes


class Alert:
    def __init__(self, service: ServiceInput, token: str, chatId: str) -> None:
        self.client: Union[WhatsappAlert, TelegramAlert, EmailAlert]

        if service == Service.WHATSAPP:
            self.client = WhatsappAlert(token, chatId)
        elif service == Service.TELEGRAM:
            self.client = TelegramAlert(token, chatId)
        elif service == Service.EMAIL:
            self.client = EmailAlert(token, chatId)
        else:
            raise Exception("Input Service is Invalid!")

    def send_one_message(self, payload: MessagePayload):
        if isinstance(self.client, WhatsappAlert):
            return self.client.send_one_message(payload["message"])

    def send_one_image(self, payload: ImagePayload):
        if isinstance(self.client, WhatsappAlert):
            return self.client.send_one_image(
                payload["message"], payload["message"]
            )

    def send_one_video(self, payload: VideoPayload):
        if isinstance(self.client, WhatsappAlert):
            return self.client.send_one_video(
                payload["message"], payload["message"]
            )


class WhatsappMessagePayload(TypedDict):
    groupId: str
    message: str


class WhatsappImagePayload(MessagePayload):
    groupId: str
    message: str
    imageBase64: str


class WhatsappVideoPayload(MessagePayload):
    groupId: str
    message: str
    videobase64: str


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

    def send_one_image(self, message: str, image_base64: str):
        return

    def send_one_video(self, message: str, video_base64: str):
        return


class TelegramAlert:
    def __init__(self, token, secret):
        return

    def send_one_message(self, message: str):
        return

    # def send_one_image(self, message: str, image_bytes: bytes):
    #     return

    def send_one_video(self, message: str, video_bytes: bytes):
        return


class EmailAlert:
    def __init__(self, token, secret):
        return

    def send_one_message(self, message: str):
        return

    # def send_one_image(self, message: str, image_bytes: bytes):
    #     return

    def send_one_video(self, message: str, video_bytes: bytes):
        return
