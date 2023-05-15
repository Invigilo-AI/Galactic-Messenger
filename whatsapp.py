import aiohttp
from config import Config
from typing import cast, Literal, List, Union
from functools import partial
from utils import compose, is_type
from pydantic import BaseModel


class WhatsappMessagePayload(BaseModel):
    groupId: str
    message: str


class WhatsappImagePayload(BaseModel):
    groupId: str
    caption: str
    imageBase64: str


class WhatsappVideoPayload(BaseModel):
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


def _get_payload_type(
    payload: AllowedSingleWhatsappPayload,
) -> Literal["MESSAGE", "IMAGE", "VIDEO"]:
    if is_type(payload, WhatsappMessagePayload):
        return "MESSAGE"
    elif is_type(payload, WhatsappImagePayload):
        return "IMAGE"
    elif is_type(payload, WhatsappImagePayload):
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
    response = await session.post(f"{ip}/{payload_type.lower()}", json=payload)
    return response


async def _send_and_parse_to_json(
    ip: str,
    session: aiohttp.ClientSession,
    payload_type: Literal["MESSAGE", "IMAGE", "VIDEO"],
    payload: AllowedSingleWhatsappPayload,
) -> str:
    return await _to_json(await _send(ip, session, payload_type, payload))


async def _get_type_and_send_single_and_parse_to_json(
    ip: str,
    session: aiohttp.ClientSession,
    payload: AllowedSingleWhatsappPayload,
):
    return await partial(
        _send_and_parse_to_json, ip=ip, session=session, payload=payload
    )(_get_payload_type(payload))


async def _send_single(
    ip: str,
    session: aiohttp.ClientSession,
    payload: AllowedSingleWhatsappPayload,
):
    return await _get_type_and_send_single_and_parse_to_json(
        ip, session, payload
    )


async def _send_multiple(
    ip: str,
    session: aiohttp.ClientSession,
    payloads: AllowedBatchWhatsappPayload,
) -> list[str]:
    return list(
        [
            await partial(
                _send_single,
                ip=ip,
                session=session,
            )(payload)
            for payload in payloads
        ],
    )


async def _handle_send(
    ip: str, session: aiohttp.ClientSession, payload: AllowedWhatsappPayload
) -> Union[str, list[str]]:
    return (
        await _send_multiple(
            ip, session, cast(AllowedBatchWhatsappPayload, payload)
        )
        if _is_batch(payload)
        else await _send_single(
            ip, session, cast(AllowedSingleWhatsappPayload, payload)
        )
    )


def _is_batch(payload: AllowedWhatsappPayload):
    return "BATCH" if type(payload) == "list" else "SINGLE"


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
        timeout=compose(_get_timeout_option, _is_batch)(payload)
    )


async def setup_whatsapp(ip: str):
    async def send_whatsapp(payload: AllowedWhatsappPayload):
        return await _handle_send(ip, _handle_create_session(payload), payload)

    return send_whatsapp
