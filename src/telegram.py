from functools import partial
from typing import List, Literal, TypedDict, Union, cast

import aiohttp

from config import Config
from src.utils import compose, is_schema


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


AllowedSingleTelegramPayload = Union[
    TelegramMessagePayload, TelegramImagePayload, TelegramVideoPayload
]

AllowedBatchTelegramPayload = List[
    Union[TelegramMessagePayload, TelegramImagePayload, TelegramVideoPayload]
]

AllowedTelegramPayload = Union[
    AllowedSingleTelegramPayload, AllowedBatchTelegramPayload
]


class TelegramMessageInput(TypedDict):
    chatId: str
    text: str


class TelegramImageInput(TypedDict):
    chatId: str
    text: str
    imageBytes: bytes


class TelegramVideoInput(TypedDict):
    chatId: str
    text: str
    videoBytes: bytes


SingleTelegramInput = Union[
    TelegramMessageInput, TelegramImageInput, TelegramVideoInput
]

BatchTelegramInput = List[
    Union[TelegramMessageInput, TelegramImageInput, TelegramVideoInput]
]

TelegramInput = Union[SingleTelegramInput, BatchTelegramInput]


def _get_payload_type(
    payload: AllowedSingleTelegramPayload,
) -> Literal["MESSAGE", "IMAGE", "VIDEO"]:
    if is_schema(payload, TelegramMessagePayload):
        return "MESSAGE"
    elif is_schema(payload, TelegramImagePayload):
        return "IMAGE"
    elif is_schema(payload, TelegramVideoPayload):
        return "VIDEO"
    else:
        raise ValueError("Invalid Input Payload")


async def _to_json(response: aiohttp.ClientResponse) -> str:
    return await response.json()


def __create_form_data(payload: AllowedSingleTelegramPayload):
    data = aiohttp.FormData()
    data.add_fields(*payload.items())
    return data


async def _send(
    token: str,
    session: aiohttp.ClientSession,
    payload_type: Literal["MESSAGE", "IMAGE", "VIDEO"],
    payload: AllowedSingleTelegramPayload,
) -> aiohttp.ClientResponse:
    response = await session.post(
        f"https://api.telegram.org/bot{token}/send{payload_type.capitalize()}",
        data=__create_form_data(payload),
    )
    return response


async def _send_and_parse_to_json(
    ip: str,
    session: aiohttp.ClientSession,
    payload_type: Literal["MESSAGE", "IMAGE", "VIDEO"],
    payload: AllowedSingleTelegramPayload,
) -> str:
    return await _to_json(await _send(ip, session, payload_type, payload))


async def _get_type_and_send_and_parse_to_json(
    ip: str,
    session: aiohttp.ClientSession,
    payload: AllowedSingleTelegramPayload,
):
    return await partial(
        _send_and_parse_to_json, ip=ip, session=session, payload=payload
    )(payload_type=_get_payload_type(payload))


async def _send_single(
    ip: str,
    session: aiohttp.ClientSession,
    payload: AllowedSingleTelegramPayload,
):
    return await _get_type_and_send_and_parse_to_json(ip, session, payload)


async def _send_multiple(
    ip: str,
    session: aiohttp.ClientSession,
    payloads: AllowedBatchTelegramPayload,
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
    ip: str, session: aiohttp.ClientSession, payload: AllowedTelegramPayload
) -> Union[str, list[str]]:
    async with session:
        return (
            await _send_multiple(
                ip, session, cast(AllowedBatchTelegramPayload, payload)
            )
            if _is_batch(payload)
            else await _send_single(
                ip, session, cast(AllowedSingleTelegramPayload, payload)
            )
        )


def _is_batch(payload: AllowedTelegramPayload) -> bool:
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


def _handle_create_session(payload: AllowedTelegramPayload):
    return aiohttp.ClientSession(
        timeout=compose(
            _get_timeout_option,
            lambda x: "BATCH" if _is_batch(x) else "SINGLE",
        )(payload)
    )


def _parse_single_input_to_payload(
    input_dict: SingleTelegramInput,
) -> AllowedSingleTelegramPayload:
    if is_schema(input_dict, TelegramImageInput):
        t_ii = cast(TelegramImageInput, input_dict)
        return {
            "chat_id": t_ii["chatId"],
            "photo": t_ii["imageBytes"],
            "caption": t_ii["text"],
        }
    elif is_schema(input_dict, TelegramVideoInput):
        t_ii = cast(TelegramVideoInput, input_dict)
        return {
            "chat_id": t_ii["chatId"],
            "video": t_ii["videoBytes"],
            "caption": t_ii["text"],
        }
    elif is_schema(input_dict, TelegramMessageInput):
        wa_mi = cast(TelegramImageInput, input_dict)
        return {
            "chat_id": wa_mi["chatId"],
            "text": wa_mi["text"],
        }
    else:
        raise ValueError("Input Schema is Invalid")


def _parse_multiple_input_to_payload(
    input_dicts: BatchTelegramInput,
) -> AllowedTelegramPayload:
    return list(map(_parse_single_input_to_payload, input_dicts))


def _handle_parse_input_to_payload(
    telegram_input: TelegramInput,
) -> AllowedTelegramPayload:
    return (
        _parse_multiple_input_to_payload(
            cast(BatchTelegramInput, telegram_input)
        )
        if isinstance(telegram_input, List)
        else _parse_single_input_to_payload(
            cast(SingleTelegramInput, telegram_input)
        )
    )


def setup_telegram(ip: str):
    async def send_telegram(telegram_input: TelegramInput):
        payload = _handle_parse_input_to_payload(telegram_input)
        return await _handle_send(ip, _handle_create_session(payload), payload)

    return send_telegram
