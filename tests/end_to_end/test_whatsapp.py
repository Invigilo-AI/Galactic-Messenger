import pytest

from env import env
from whatsapp import setup_whatsapp


@pytest.mark.asyncio
async def test_send_whatsapp_message():
    send_whatsapp = setup_whatsapp(env.TEST_WHATSAPP_IP)
    res = await send_whatsapp(
        {"groupId": env.TEST_WHATSAPP_GROUP_ID, "message": "Hello World!"}
    )
    assert res


@pytest.mark.asyncio
async def test_send_whatsapp_image():
    send_whatsapp = setup_whatsapp(env.TEST_WHATSAPP_IP)
    res = await send_whatsapp(
        {
            "groupId": env.TEST_WHATSAPP_GROUP_ID,
            "imageBytes": open("tests/data/SampleImage.jpg", "rb").read(),
            "caption": "Hello World!",
        }
    )
    assert res


@pytest.mark.asyncio
async def test_send_whatsapp_video():
    send_whatsapp = setup_whatsapp(env.TEST_WHATSAPP_IP)
    res = await send_whatsapp(
        {
            "groupId": env.TEST_WHATSAPP_GROUP_ID,
            "videoBytes": open("tests/data/SampleVideo.mp4", "rb").read(),
            "caption": "Hello World!",
        }
    )
    assert res


@pytest.mark.asyncio
async def test_send_whatsapp_batch_mixed():
    send_whatsapp = setup_whatsapp(env.TEST_WHATSAPP_IP)
    res = await send_whatsapp(
        [
            {
                "groupId": env.TEST_WHATSAPP_GROUP_ID,
                "message": "Yoooo",
            },
            {
                "groupId": env.TEST_WHATSAPP_GROUP_ID,
                "videoBytes": open("tests/data/SampleVideo.mp4", "rb").read(),
                "caption": "!!!!",
            },
            {
                "groupId": env.TEST_WHATSAPP_GROUP_ID,
                "imageBytes": open("tests/data/SampleImage.jpg", "rb").read(),
                "caption": "Hello World!",
            },
            {
                "groupId": env.TEST_WHATSAPP_GROUP_ID,
                "message": "🎉 Congratulations on passing the WhatsApp messaging test with flying colors! 🚀 Your skills are on fire, and your code is sending messages, photos, videos, and even mixed batches flawlessly! 😄 Keep up the amazing work, and keep spreading smiles with your fantastic creations! 💪🌟",
            },
        ]
    )
    assert res
