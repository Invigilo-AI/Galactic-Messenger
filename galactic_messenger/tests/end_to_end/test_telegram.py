import pytest

from ...env.env import env
from ...src.telegram import setup_telegram


@pytest.mark.asyncio
async def test_send_telegram_message():
    send_telegram = setup_telegram(env.TEST_TELEGRAM_TOKEN)
    res = await send_telegram(
        {"chatId": env.TEST_TELEGRAM_CHAT_ID, "text": "Hello World!"}
    )
    assert res


@pytest.mark.asyncio
async def test_send_telegram_image():
    send_telegram = setup_telegram(env.TEST_TELEGRAM_TOKEN)
    res = await send_telegram(
        {
            "chatId": env.TEST_TELEGRAM_CHAT_ID,
            "imageBytes": open("tests/data/SampleImage.jpg", "rb").read(),
            "text": "Hello World!",
        }
    )
    assert res


@pytest.mark.asyncio
async def test_send_telegram_video():
    send_telegram = setup_telegram(env.TEST_TELEGRAM_TOKEN)
    res = await send_telegram(
        {
            "chatId": env.TEST_TELEGRAM_CHAT_ID,
            "videoBytes": open("tests/data/SampleVideo.mp4", "rb").read(),
            "text": "Hello World!",
        }
    )
    assert res


@pytest.mark.asyncio
async def test_send_telegram_batch_mixed():
    send_telegram = setup_telegram(env.TEST_TELEGRAM_TOKEN)
    res = await send_telegram(
        [
            {
                "chatId": env.TEST_TELEGRAM_TOKEN,
                "text": "Yoooo",
            },
            {
                "chatId": env.TEST_TELEGRAM_CHAT_ID,
                "videoBytes": open("tests/data/SampleVideo.mp4", "rb").read(),
                "text": "!!!!",
            },
            {
                "chatId": env.TEST_TELEGRAM_CHAT_ID,
                "imageBytes": open("tests/data/SampleImage.jpg", "rb").read(),
                "text": "Hello World!",
            },
            {
                "chatId": env.TEST_TELEGRAM_CHAT_ID,
                "text": "🎉 Congratulations on passing the telegram messaging test with flying colors! 🚀 Your skills are on fire, and your code is sending messages, photos, videos, and even mixed batches flawlessly! 😄 Keep up the amazing work, and keep spreading smiles with your fantastic creations! 💪🌟",
            },
        ]
    )
    assert res
