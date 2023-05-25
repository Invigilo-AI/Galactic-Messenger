from typing import TypedDict
from unittest.mock import AsyncMock

import pytest
from aiohttp import ClientSession

from galactic_messenger.src.whatsapp import (
    _bytes_to_base64, _get_payload_type, _get_timeout_option,
    _get_type_and_send_and_parse_to_json, _handle_create_session,
    _handle_parse_input_to_payload, _handle_send, _is_batch,
    _parse_multiple_input_to_payload, _parse_single_input_to_payload, _send,
    _send_and_parse_to_json, _send_multiple, _send_single, _to_json,
    setup_whatsapp)


@pytest.mark.asyncio
async def test_get_payload_type():
    class PayloadMessage(TypedDict):
        groupId: str
        message: str

    payload: PayloadMessage = {"groupId": "groupId", "message": "Hello"}
    assert _get_payload_type(payload) == "MESSAGE"

    class PayloadImage(TypedDict):
        groupId: str
        caption: str
        imageBase64: str

    payload2: PayloadImage = {
        "groupId": "groupId",
        "caption": "Image",
        "imageBase64": "base64_string",
    }
    assert _get_payload_type(payload2) == "IMAGE"

    class PayloadVideo(TypedDict):
        groupId: str
        caption: str
        videoBase64: str

    payload3: PayloadVideo = {
        "groupId": "chatId",
        "caption": "Video",
        "videoBase64": "base64_string",
    }
    assert _get_payload_type(payload3) == "VIDEO"


@pytest.mark.asyncio
async def test_to_json():
    response = AsyncMock()
    response.json = AsyncMock(return_value="json_response")

    assert await _to_json(response) == "json_response"
    response.json.assert_called_once()


@pytest.mark.asyncio
async def test_send():
    class PayloadMessage(TypedDict):
        groupId: str
        message: str

    ip = "example.com"
    session = AsyncMock()
    payload_type = "MESSAGE"

    payload: PayloadMessage = {"groupId": "chatId", "message": "Hello"}

    response = AsyncMock()
    session.post = AsyncMock(return_value=response)

    assert await _send(ip, session, payload_type, payload) == response
    session.post.assert_called_once_with(
        f"{ip}/sendWhatsapp/{payload_type.lower()}", json=payload
    )


@pytest.mark.asyncio
async def test_send_and_parse_to_json():
    class PayloadMessage(TypedDict):
        groupId: str
        message: str

    ip = "example.com"
    session = AsyncMock()
    payload_type = "MESSAGE"

    payload: PayloadMessage = {"groupId": "groupId", "message": "Hello"}

    response = AsyncMock()
    response.json = AsyncMock(return_value="json_response")
    session.post = AsyncMock(return_value=response)

    assert (
        await _send_and_parse_to_json(ip, session, payload_type, payload)
        == "json_response"
    )
    session.post.assert_called_once_with(
        f"{ip}/sendWhatsapp/{payload_type.lower()}", json=payload
    )
    response.json.assert_called_once()
