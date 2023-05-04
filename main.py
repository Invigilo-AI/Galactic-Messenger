from typing import TypedDict, Literal, Union
from functools import partial
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
    def __init__(self, service: ServiceInput, token: str) -> None:
        self.client: Union[WhatsappAlert, TelegramAlert, EmailAlert]

        if service == Service.WHATSAPP:
            self.client = WhatsappAlert(token)
        elif service == Service.TELEGRAM:
            self.client = TelegramAlert(token)
        elif service == Service.EMAIL:
            self.client = EmailAlert(token)
        else:
            raise Exception("Input Service is Invalid!")

    def __bytes_2_base64_str(self, b: bytes):
        return base64.b64encode(b).decode("utf-8")

    async def send_one_message(self, to: str, payload: MessagePayload):
        if isinstance(self.client, WhatsappAlert):
            return await self.client.send_one_message(to, payload["message"])

    async def send_one_image(self, to: str, payload: ImagePayload):
        if isinstance(self.client, WhatsappAlert):
            return await self.client.send_one_image(
                to,
                payload["message"],
                self.__bytes_2_base64_str(payload["image_bytes"]),
            )

    async def send_one_video(self, to: str, payload: VideoPayload):
        if isinstance(self.client, WhatsappAlert):
            return await self.client.send_one_video(
                to,
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


AllowedWhatsappPayload = Union[
    WhatsappMessagePayload, WhatsappImagePayload, WhatsappVideoPayload
]


class WhatsappAlert:
    def __init__(self, ip: str):
        self.url = f"http://{ip}:5000/sendWhatsapp"

    async def __send(
        self,
        session: aiohttp.ClientSession,
        payload_type: Literal["MESSAGE", "IMAGE", "VIDEO"],
        payload: AllowedWhatsappPayload,
    ):
        response = await session.post(
            f"{self.url}/{payload_type.lower()}", json=json.dumps(payload)
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
        self, groupId: str, message: str, image_base64: str
    ):
        return await self.__send_one(
            "IMAGE",
            {
                "groupId": groupId,
                "message": message,
                "imageBase64": image_base64,
            },
        )

    async def send_one_video(
        self, groupId: str, message: str, image_base64: str
    ):
        return await self.__send_one(
            "VIDEO",
            {
                "groupId": groupId,
                "message": message,
                "imageBase64": image_base64,
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
        messages: list[str],
        images_base64: list[str],
    ):
        return await self.__send_many(
            "IMAGE",
            [
                {
                    "groupId": groupId,
                    "message": message,
                    "imageBase64": image_base64,
                }
                for groupId, message, image_base64 in zip(
                    groupIds, messages, images_base64
                )
            ],
        )

    async def send_many_videos(
        self,
        groupIds: list[str],
        messages: list[str],
        videos_base64: list[str],
    ):
        return await self.__send_many(
            "VIDEO",
            [
                {
                    "groupId": groupId,
                    "message": message,
                    "videoBase64": video_base64,
                }
                for groupId, message, video_base64 in zip(
                    groupIds, messages, videos_base64
                )
            ],
        )

    # async def send_one_message(self, message: str):
    #     timeout_options = aiohttp.ClientTimeout(
    #         total=Config.SINGLE_TOTAL_TIMEOUT.value
    #     )
    #     client = aiohttp.ClientSession(timeout=timeout_options)
    #     payload: WhatsappMessagePayload = {
    #         "groupId": self.groupId,
    #         "message": message,
    #     }
    #     response = await client.post(
    #         self.url + "/message", json=json.dumps(payload)
    #     )
    #     response_json = await response.json()
    #     await client.close()
    #     return response_json

    # async def send_one_image(self, message: str, image_base64: str):
    #     timeout_options = aiohttp.ClientTimeout(
    #         total=Config.SINGLE_TOTAL_TIMEOUT.value,
    #         connect=Config.SINGLE_CONNECT_TIMEOUT.value,
    #     )
    #     client = aiohttp.ClientSession(timeout=timeout_options)
    #     payload: WhatsappImagePayload = {
    #         "groupId": self.groupId,
    #         "message": message,
    #         "imageBase64": image_base64,
    #     }
    #     response = await client.post(
    #         self.url + "/image", json=json.dumps(payload)
    #     )
    #     response_json = await response.json()
    #     await client.close()
    #     return response_json

    # async def send_one_video(self, message: str, video_base64: str):
    #     timeout_options = aiohttp.ClientTimeout(
    #         total=Config.SINGLE_TOTAL_TIMEOUT.value,
    #         connect=Config.SINGLE_CONNECT_TIMEOUT.value,
    #     )
    #     client = aiohttp.ClientSession(timeout=timeout_options)
    #     payload: WhatsappVideoPayload = {
    #         "groupId": self.groupId,
    #         "message": message,
    #         "videoBase64": video_base64,
    #     }
    #     response = await client.post(
    #         self.url + "/video", json=json.dumps(payload)
    #     )
    #     response_json = await response.json()
    #     await client.close()
    #     return response_json

    # async def send_many_messages(self, messages: list[str]):
    #     timeout_options = aiohttp.ClientTimeout(
    #         total=Config.BATCH_TOTAL_TIMEOUT.value,
    #         connect=Config.BATCH_CONNECT_TIMEOUT.value,
    #     )
    #     client = aiohttp.ClientSession(timeout=timeout_options)
    #
    #     responses_json = []
    #     for message in messages:
    #         payload: WhatsappMessagePayload = {
    #             "groupId": self.groupId,
    #             "message": message,
    #         }
    #         response = await client.post(
    #             self.url + "/message", json=json.dumps(payload)
    #         )
    #         response_json = await response.json()
    #         response_json.append(response_json)
    #
    #     await client.close()
    #     return responses_json
    #
    # async def send_many_images(
    #     self, messages: list[str], images_base64: list[str]
    # ):
    #     timeout_options = aiohttp.ClientTimeout(
    #         total=Config.BATCH_TOTAL_TIMEOUT.value,
    #         connect=Config.BATCH_CONNECT_TIMEOUT.value,
    #     )
    #     client = aiohttp.ClientSession(timeout=timeout_options)
    #
    #     responses_json = []
    #     for message, image_base64 in zip(messages, images_base64):
    #         payload: WhatsappImagePayload = {
    #             "groupId": self.groupId,
    #             "message": message,
    #             "imageBase64": image_base64,
    #         }
    #         response = await client.post(
    #             self.url + "/image", json=json.dumps(payload)
    #         )
    #         response_json = await response.json()
    #         response_json.append(response_json)
    #
    #     await client.close()
    #     return responses_json
    #
    # async def send_many_videos(
    #     self, messages: list[str], videos_base64: list[str]
    # ):
    #     timeout_options = aiohttp.ClientTimeout(
    #         total=Config.BATCH_TOTAL_TIMEOUT.value,
    #         connect=Config.BATCH_CONNECT_TIMEOUT.value,
    #     )
    #     client = aiohttp.ClientSession(timeout=timeout_options)
    #
    #     async def send(
    #         message: str,
    #         video_base64: str,
    #     ):
    #         payload: WhatsappVideoPayload = {
    #             "groupId": self.groupId,
    #             "message": message,
    #             "videoBase64": video_base64,
    #         }
    #         response = await client.post(
    #             self.url + "/video", json=json.dumps(payload)
    #         )
    #         return await response.json()
    #
    #     responses_json = map(send, messages, videos_base64)
    #
    #     await client.close()
    #     return responses_json


class TelegramAlert:
    def __init__(self, token):
        return

    def send_one_message(self, message: str):
        return

    def send_one_image(self, message: str, image_bytes: bytes):
        return

    def send_one_video(self, message: str, video_bytes: bytes):
        return


class EmailAlert:
    def __init__(self, token):
        return

    def send_one_message(self, message: str):
        return

    def send_one_image(self, message: str, image_bytes: bytes):
        return

    def send_one_video(self, message: str, video_bytes: bytes):
        return


if __name__ == "__main__":

    async def main():
        wa_alert = Alert("WHATSAPP", "tokenabc")
        await wa_alert.send_one_image(
            "groupA", {"message": "hi", "image_bytes": b"zxc"}
        )

    result = main()
