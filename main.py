from typing import TypedDict, Literal, Union
from functools import partial
from enum import Enum
import aiohttp
import base64


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
    caption: str
    image_bytes: bytes


class VideoPayload(TypedDict):
    caption: str
    video_bytes: bytes


class Alert:
    def __init__(self, service: ServiceInput, token: str) -> None:
        self.client: Union[WhatsappAlert, TelegramAlert, EmailAlert]

        if service == Service.WHATSAPP.value:
            self.client = WhatsappAlert(token)
        elif service == Service.TELEGRAM.value:
            self.client = TelegramAlert(token)
        elif service == Service.EMAIL.value:
            self.client = EmailAlert(token)
        else:
            raise Exception("Input Service is Invalid!")

    def __bytes_2_base64_str(self, b: bytes):
        return base64.b64encode(b).decode("utf-8")

    async def send_one_message(self, to: str, payload: MessagePayload):
        if isinstance(self.client, WhatsappAlert):
            return await self.client.send_one_message(to, payload["message"])
        if isinstance(self.client, TelegramAlert):
            return await self.client.send_one_message(to, payload["message"])

    async def send_one_image(self, to: str, payload: ImagePayload):
        if isinstance(self.client, WhatsappAlert):
            return await self.client.send_one_image(
                to,
                payload["caption"],
                self.__bytes_2_base64_str(payload["image_bytes"]),
            )
        if isinstance(self.client, TelegramAlert):
            return await self.client.send_one_image(
                to, payload["caption"], payload["image_bytes"]
            )

    async def send_one_video(self, to: str, payload: VideoPayload):
        if isinstance(self.client, WhatsappAlert):
            return await self.client.send_one_video(
                to,
                payload["caption"],
                self.__bytes_2_base64_str(payload["video_bytes"]),
            )
        if isinstance(self.client, TelegramAlert):
            return await self.client.send_one_video(
                to, payload["caption"], payload["video_bytes"]
            )


class WhatsappMessagePayload(TypedDict):
    groupId: str
    message: str


class WhatsappImagePayload(TypedDict):
    groupId: str
    caption: str
    imageBase64: str


class WhatsappVideoPayload(TypedDict):
    groupId: str
    caption: str
    videoBase64: str


AllowedWhatsappPayload = Union[
    WhatsappMessagePayload, WhatsappImagePayload, WhatsappVideoPayload
]


class WhatsappAlert:
    def __init__(self, ip: str):
        self.url = f"http://{ip}:3000/sendWhatsapp"

    async def __send(
        self,
        session: aiohttp.ClientSession,
        payload_type: Literal["MESSAGE", "IMAGE", "VIDEO"],
        payload: AllowedWhatsappPayload,
    ):
        response = await session.post(
            f"{self.url}/{payload_type.lower()}", json=payload
        )
        return await response.json()

    async def __send_one(
        self,
        payload_type: Literal["MESSAGE", "IMAGE", "VIDEO"],
        payload: AllowedWhatsappPayload,
    ):
        timeout_options = aiohttp.ClientTimeout(
            total=Config.SINGLE_TOTAL_TIMEOUT.value,
            connect=Config.SINGLE_CONNECT_TIMEOUT.value,
        )
        session = aiohttp.ClientSession(timeout=timeout_options)
        response_json = await self.__send(session, payload_type, payload)
        await session.close()
        return response_json

    async def __send_many(
        self,
        payload_type: Literal["MESSAGE", "IMAGE", "VIDEO"],
        payloads: list[AllowedWhatsappPayload],
    ):
        timeout_options = aiohttp.ClientTimeout(
            total=Config.BATCH_TOTAL_TIMEOUT.value,
            connect=Config.BATCH_CONNECT_TIMEOUT.value,
        )
        session = aiohttp.ClientSession(timeout=timeout_options)
        response_json = map(
            partial(self.__send, session=session, payload_type=payload_type),
            payloads,
        )
        await session.close()
        return response_json

    async def send_one_message(self, groupId: str, message: str):
        return await self.__send_one(
            "MESSAGE", {"groupId": groupId, "message": message}
        )

    async def send_one_image(
        self, groupId: str, caption: str, image_base64: str
    ):
        return await self.__send_one(
            "IMAGE",
            {
                "groupId": groupId,
                "caption": caption,
                "imageBase64": image_base64,
            },
        )

    async def send_one_video(
        self, groupId: str, caption: str, video_base64: str
    ):
        return await self.__send_one(
            "VIDEO",
            {
                "groupId": groupId,
                "caption": caption,
                "videoBase64": video_base64,
            },
        )

    async def send_many_messages(
        self, groupIds: list[str], messages: list[str]
    ):
        return await self.__send_many(
            "MESSAGE",
            [
                {"groupId": groupId, "message": message}
                for groupId, message in zip(groupIds, messages)
            ],
        )

    async def send_many_images(
        self,
        groupIds: list[str],
        captions: list[str],
        images_base64: list[str],
    ):
        return await self.__send_many(
            "IMAGE",
            [
                {
                    "groupId": groupId,
                    "caption": caption,
                    "imageBase64": image_base64,
                }
                for groupId, caption, image_base64 in zip(
                    groupIds, captions, images_base64
                )
            ],
        )

    async def send_many_videos(
        self,
        groupIds: list[str],
        captions: list[str],
        videos_base64: list[str],
    ):
        return await self.__send_many(
            "VIDEO",
            [
                {
                    "groupId": groupId,
                    "caption": caption,
                    "videoBase64": video_base64,
                }
                for groupId, caption, video_base64 in zip(
                    groupIds, captions, videos_base64
                )
            ],
        )


class TelegramMessagePayload(TypedDict):
    chat_id: str
    text: str


class TelegramImagePayload(TypedDict):
    chat_id: str
    photo: bytes
    caption: str


class TelegramVideoPayload(TypedDict):
    chat_id: str
    video: bytes
    caption: str


AllowedTelegramPayload = Union[
    TelegramMessagePayload, TelegramImagePayload, TelegramVideoPayload
]


class TelegramAlert:
    def __init__(self, token: str):
        self.url = f"https://api.telegram.org/bot{token}"

    def __create_form_data(self, payload: AllowedTelegramPayload):
        data = aiohttp.FormData()
        data.add_fields(*payload.items())
        return data

    async def __send(
        self,
        session: aiohttp.ClientSession,
        payload_type: Literal["sendMessage", "sendPhoto", "sendVideo"],
        payload: AllowedTelegramPayload,
    ):
        response = await session.post(
            f"{self.url}/{payload_type}",
            data=self.__create_form_data(payload),
        )
        return await response.read()

    async def __send_one(
        self,
        payload_type: Literal["sendMessage", "sendPhoto", "sendVideo"],
        payload: AllowedTelegramPayload,
    ):
        timeout_options = aiohttp.ClientTimeout(
            total=Config.SINGLE_TOTAL_TIMEOUT.value,
            connect=Config.SINGLE_CONNECT_TIMEOUT.value,
        )
        session = aiohttp.ClientSession(timeout=timeout_options)
        response_json = await self.__send(session, payload_type, payload)
        await session.close()
        return response_json

    async def __send_many(
        self,
        payload_type: Literal["sendMessage", "sendPhoto", "sendVideo"],
        payloads: list[AllowedTelegramPayload],
    ):
        timeout_options = aiohttp.ClientTimeout(
            total=Config.BATCH_TOTAL_TIMEOUT.value,
            connect=Config.BATCH_CONNECT_TIMEOUT.value,
        )
        session = aiohttp.ClientSession(timeout=timeout_options)
        response_json = map(
            partial(self.__send, session=session, payload_type=payload_type),
            payloads,
        )
        await session.close()
        return response_json

    async def send_one_message(self, chat_id: str, text: str):
        return await self.__send_one(
            "sendMessage", {"chat_id": chat_id, "text": text}
        )

    async def send_one_image(self, chat_id: str, caption: str, photo: bytes):
        return await self.__send_one(
            "sendPhoto",
            {
                "chat_id": chat_id,
                "caption": caption,
                "photo": photo,
            },
        )

    async def send_one_video(self, chat_id: str, caption: str, video: bytes):
        return await self.__send_one(
            "sendVideo",
            {
                "chat_id": chat_id,
                "caption": caption,
                "video": video,
            },
        )

    async def send_many_messages(self, chat_ids: list[str], texts: list[str]):
        return await self.__send_many(
            "sendMessage",
            [
                {"chat_id": chat_id, "text": text}
                for chat_id, text in zip(chat_ids, texts)
            ],
        )

    async def send_many_images(
        self,
        chat_ids: list[str],
        captions: list[str],
        photos: list[bytes],
    ):
        return await self.__send_many(
            "sendPhoto",
            [
                {
                    "chat_id": chat_id,
                    "caption": caption,
                    "photo": photo,
                }
                for chat_id, caption, photo in zip(chat_ids, captions, photos)
            ],
        )

    async def send_many_videos(
        self,
        chat_ids: list[str],
        captions: list[str],
        videos: list[bytes],
    ):
        return await self.__send_many(
            "sendVideo",
            [
                {
                    "chat_id": chat_id,
                    "caption": caption,
                    "video": video,
                }
                for chat_id, caption, video in zip(chat_ids, captions, videos)
            ],
        )


class EmailAlert:
    def __init__(self, token):
        return

    def send_one_message(self, message: str):
        return

    def send_one_image(self, message: str, image_bytes: bytes):
        return

    def send_one_video(self, message: str, video_bytes: bytes):
        return
