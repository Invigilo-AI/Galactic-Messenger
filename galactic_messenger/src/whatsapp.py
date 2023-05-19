import base64
from functools import partial
from typing import List, Literal, TypedDict, Union, cast

import aiohttp

from ..config import Config
from ..src.utils import compose, is_schema


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


AllowedSingleWhatsappPayload = Union[
    WhatsappMessagePayload, WhatsappImagePayload, WhatsappVideoPayload
]

AllowedBatchWhatsappPayload = List[
    Union[WhatsappMessagePayload, WhatsappImagePayload, WhatsappVideoPayload]
]

AllowedWhatsappPayload = Union[
    AllowedSingleWhatsappPayload, AllowedBatchWhatsappPayload
]


class WhatsappMessageInput(TypedDict):
    chatId: str
    text: str


class WhatsappImageInput(TypedDict):
    chatId: str
    text: str
    imageBytes: bytes


class WhatsappVideoInput(TypedDict):
    chatId: str
    text: str
    videoBytes: bytes


SingleWhatsappInput = Union[
    WhatsappMessageInput, WhatsappImageInput, WhatsappVideoInput
]

BatchWhatsappInput = List[
    Union[WhatsappMessageInput, WhatsappImageInput, WhatsappVideoInput]
]

WhatsappInput = Union[SingleWhatsappInput, BatchWhatsappInput]


def _get_payload_type(
    payload: AllowedSingleWhatsappPayload,
) -> Literal["MESSAGE", "IMAGE", "VIDEO"]:
    if is_schema(payload, WhatsappMessagePayload):
        return "MESSAGE"
    elif is_schema(payload, WhatsappImagePayload):
        return "IMAGE"
    elif is_schema(payload, WhatsappVideoPayload):
        return "VIDEO"
    else:
        raise ValueError("Invalid Input Payload")


async def _to_json(response: aiohttp.ClientResponse) -> str:
    return await response.json()


async def _send(
    ip: str,
    session: aiohttp.ClientSession,
    payload_type: Literal["MESSAGE", "IMAGE", "VIDEO"],
    payload: AllowedSingleWhatsappPayload,
) -> aiohttp.ClientResponse:
    response = await session.post(
        f"{ip}/sendWhatsapp/{payload_type.lower()}", json=payload
    )
    return response


async def _send_and_parse_to_json(
    ip: str,
    session: aiohttp.ClientSession,
    payload_type: Literal["MESSAGE", "IMAGE", "VIDEO"],
    payload: AllowedSingleWhatsappPayload,
) -> str:
    return await _to_json(await _send(ip, session, payload_type, payload))


async def _get_type_and_send_and_parse_to_json(
    ip: str,
    session: aiohttp.ClientSession,
    payload: AllowedSingleWhatsappPayload,
):
    return await partial(
        _send_and_parse_to_json, ip=ip, session=session, payload=payload
    )(payload_type=_get_payload_type(payload))


async def _send_single(
    ip: str,
    session: aiohttp.ClientSession,
    payload: AllowedSingleWhatsappPayload,
):
    return await _get_type_and_send_and_parse_to_json(ip, session, payload)


async def _send_multiple(
    ip: str,
    session: aiohttp.ClientSession,
    payloads: AllowedBatchWhatsappPayload,
) -> list[str]:
    return [
        await partial(
            _send_single,
            ip=ip,
            session=session,
        )(payload=payload)
        for payload in payloads
    ]


async def _handle_send(
    ip: str, session: aiohttp.ClientSession, payload: AllowedWhatsappPayload
) -> Union[str, list[str]]:
    async with session:
        return (
            await _send_multiple(
                ip, session, cast(AllowedBatchWhatsappPayload, payload)
            )
            if _is_batch(payload)
            else await _send_single(
                ip, session, cast(AllowedSingleWhatsappPayload, payload)
            )
        )


def _is_batch(payload: AllowedWhatsappPayload) -> bool:
    return True if isinstance(payload, List) else False


def _get_timeout_option(
    timeout_type: Literal["SINGLE", "BATCH"],
) -> aiohttp.ClientTimeout:
    return (
        aiohttp.ClientTimeout(
            total=Config.BATCH_TOTAL_TIMEOUT,
            connect=Config.BATCH_CONNECT_TIMEOUT,
        )
        if timeout_type == "BATCH"
        else aiohttp.ClientTimeout(
            total=Config.SINGLE_TOTAL_TIMEOUT,
            connect=Config.SINGLE_CONNECT_TIMEOUT,
        )
    )


def _handle_create_session(payload: AllowedWhatsappPayload):
    return aiohttp.ClientSession(
        timeout=compose(
            _get_timeout_option,
            lambda x: "BATCH" if _is_batch(x) else "SINGLE",
        )(payload)
    )


def _bytes_to_base64(b: bytes) -> str:
    return base64.b64encode(b).decode("utf-8")


def _parse_single_input_to_payload(
    input_dict: SingleWhatsappInput,
) -> AllowedSingleWhatsappPayload:
    if is_schema(input_dict, WhatsappImageInput):
        wa_ii = cast(WhatsappImageInput, input_dict)
        return {
            "groupId": wa_ii["chatId"],
            "imageBase64": _bytes_to_base64(wa_ii["imageBytes"]),
            "caption": wa_ii["text"],
        }
    elif is_schema(input_dict, WhatsappVideoInput):
        wa_ii = cast(WhatsappVideoInput, input_dict)
        return {
            "groupId": wa_ii["chatId"],
            "videoBase64": _bytes_to_base64(wa_ii["videoBytes"]),
            "caption": wa_ii["text"],
        }
    elif is_schema(input_dict, WhatsappMessageInput):
        wa_mi = cast(WhatsappMessageInput, input_dict)
        return {
            "groupId": wa_mi["chatId"],
            "message": wa_mi["text"],
        }
    else:
        raise ValueError("Input Schema is Invalid")


def _parse_multiple_input_to_payload(
    input_dicts: BatchWhatsappInput,
) -> AllowedBatchWhatsappPayload:
    return list(map(_parse_single_input_to_payload, input_dicts))


def _handle_parse_input_to_payload(
    whatsapp_input: WhatsappInput,
) -> AllowedWhatsappPayload:
    return (
        _parse_multiple_input_to_payload(
            cast(BatchWhatsappInput, whatsapp_input)
        )
        if isinstance(whatsapp_input, List)
        else _parse_single_input_to_payload(
            cast(SingleWhatsappInput, whatsapp_input)
        )
    )


def setup_whatsapp(ip: str):
    async def send_whatsapp(whatsapp_input: WhatsappInput):
        payload = _handle_parse_input_to_payload(whatsapp_input)
        return await _handle_send(ip, _handle_create_session(payload), payload)

    return send_whatsapp
