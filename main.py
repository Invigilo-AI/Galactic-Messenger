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

    def __bytes_2_base64_str(self, b: bytes):
        return base64.b64encode(b).decode("utf-8")

    async def send_one_message(self, payload: MessagePayload):
        if isinstance(self.client, WhatsappAlert):
            return await self.client.send_one_message(payload["message"])

    async def send_one_image(self, payload: ImagePayload):
        if isinstance(self.client, WhatsappAlert):
            return await self.client.send_one_image(
                payload["message"],
                self.__bytes_2_base64_str(payload["image_bytes"]),
            )

    async def send_one_video(self, payload: VideoPayload):
        if isinstance(self.client, WhatsappAlert):
            return await self.client.send_one_video(
                payload["message"],
                self.__bytes_2_base64_str(payload["video_bytes"]),
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
    videoBase64: str


class WhatsappAlert:
    def __init__(self, ip: str, groupId: str):
        self.url = f"http://{ip}:5000/sendWhatsapp"
        self.groupId = groupId

    async def send_one_message(self, message: str):
        timeout_options = aiohttp.ClientTimeout(
            total=Config.SINGLE_TOTAL_TIMEOUT.value
        )
        client = aiohttp.ClientSession(timeout=timeout_options)
        payload: WhatsappMessagePayload = {
            "groupId": self.groupId,
            "message": message,
        }
        response = await client.post(
            self.url + "/message", json=json.dumps(payload)
        )
        response_json = await response.json()
        await client.close()
        return response_json

    async def send_one_image(self, message: str, image_base64: str):
        timeout_options = aiohttp.ClientTimeout(
            total=Config.SINGLE_TOTAL_TIMEOUT.value,
            connect=Config.SINGLE_CONNECT_TIMEOUT.value,
        )
        client = aiohttp.ClientSession(timeout=timeout_options)
        payload: WhatsappImagePayload = {
            "groupId": self.groupId,
            "message": message,
            "imageBase64": image_base64,
        }
        response = await client.post(
            self.url + "/image", json=json.dumps(payload)
        )
        response_json = await response.json()
        await client.close()
        return response_json

    async def send_one_video(self, message: str, video_base64: str):
        timeout_options = aiohttp.ClientTimeout(
            total=Config.SINGLE_TOTAL_TIMEOUT.value,
            connect=Config.SINGLE_CONNECT_TIMEOUT.value,
        )
        client = aiohttp.ClientSession(timeout=timeout_options)
        payload: WhatsappVideoPayload = {
            "groupId": self.groupId,
            "message": message,
            "videoBase64": video_base64,
        }
        response = await client.post(
            self.url + "/video", json=json.dumps(payload)
        )
        response_json = await response.json()
        await client.close()
        return response_json

    async def send_many_messages(self, messages: list[str]):
        timeout_options = aiohttp.ClientTimeout(
            total=Config.BATCH_TOTAL_TIMEOUT.value,
            connect=Config.BATCH_CONNECT_TIMEOUT.value,
        )
        client = aiohttp.ClientSession(timeout=timeout_options)

        responses_json = []
        for message in messages:
            payload: WhatsappMessagePayload = {
                "groupId": self.groupId,
                "message": message,
            }
            response = await client.post(
                self.url + "/message", json=json.dumps(payload)
            )
            response_json = await response.json()
            response_json.append(response_json)

        await client.close()
        return responses_json

    async def send_many_images(
        self, messages: list[str], images_base64: list[str]
    ):
        timeout_options = aiohttp.ClientTimeout(
            total=Config.BATCH_TOTAL_TIMEOUT.value,
            connect=Config.BATCH_CONNECT_TIMEOUT.value,
        )
        client = aiohttp.ClientSession(timeout=timeout_options)

        responses_json = []
        for message, image_base64 in zip(messages, images_base64):
            payload: WhatsappImagePayload = {
                "groupId": self.groupId,
                "message": message,
                "imageBase64": image_base64,
            }
            response = await client.post(
                self.url + "/message", json=json.dumps(payload)
            )
            response_json = await response.json()
            response_json.append(response_json)

        await client.close()
        return responses_json

    async def send_many_videos(
        self, messages: list[str], videos_base64: list[str]
    ):
        timeout_options = aiohttp.ClientTimeout(
            total=Config.BATCH_TOTAL_TIMEOUT.value,
            connect=Config.BATCH_CONNECT_TIMEOUT.value,
        )
        client = aiohttp.ClientSession(timeout=timeout_options)

        responses_json = []
        for message, video_base64 in zip(messages, videos_base64):
            payload: WhatsappVideoPayload = {
                "groupId": self.groupId,
                "message": message,
                "videoBase64": video_base64,
            }
            response = await client.post(
                self.url + "/message", json=json.dumps(payload)
            )
            response_json = await response.json()
            response_json.append(response_json)

        await client.close()
        return responses_json


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
