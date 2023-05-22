# Galactic Messenger 🚀

Galactic Messenger is a versatile and efficient Python package designed for sending messages across multiple platforms. It provides seamless integration with popular communication channels such as email, Telegram, and WhatsApp, offering a streamlined solution for message delivery. Built with asynchronous capabilities, Galactic Messenger supports batch requests and delivers optimal performance. 💬📨📱

## Installation

To install Galactic Messenger, simply use pip:

```shell
pip install galactic-messenger
```

## Usage

Here is an example demonstrating how to use Galactic Messenger to send messages: 📝🚀

```python
import asyncio
from galactic_messenger import setup_email
from galactic_messenger import setup_telegram
from galactic_messenger import setup_whatsapp

async def send_messages():
    # Set up email
    email_sender = setup_email("your_email@example.com", "your_password")
    await email_sender({
        "to": "recipient@example.com",
        "subject": "Hello",
        "message": "This is a test email.",
    })

    # Set up Telegram
    telegram_sender = setup_telegram("your_telegram_token")
    await telegram_sender({
        "chatId": "your_chat_id",
        "text": "Hello from Galactic Messenger!",
    })

    # Set up WhatsApp
    whatsapp_sender = setup_whatsapp("http://your-whatsapp-api-endpoint")
    await whatsapp_sender({
        "chatId": "your_group_id",
        "text": "Hello from Galactic Messenger!",
    })

asyncio.run(send_messages())
```

## Features

### Email ✉️

- Send plain text emails
- Send emails with attachments
- Supports popular email services like Zoho Mail and Gmail

### Telegram 📢

- Send text messages to Telegram chats
- Send images with captions to Telegram chats
- Send videos with captions to Telegram chats

### WhatsApp 📲

- Send text messages to WhatsApp groups
- Send images with captions to WhatsApp groups
- Send videos with captions to WhatsApp groups

### Batch Requests 🚀

Galactic Messenger seamlessly handles batch requests, allowing you to send multiple messages simultaneously. You can provide an array of messages to the sender functions for efficient batch processing.

```python
async def main():
    # Sending multiple Telegram messages in a batch
    telegram_sender = setup_telegram("your_telegram_token")
    await telegram_sender(
        [
            {
                "chatId": "chat_id_1",
                "text": "Message 1",
            },
            {
                "chatId": "chat_id_2",
                "text": "Message 2",
                "imageBytes": open("./image.png", "rb").read(),
            },
            {
                "chatId": "chat_id_3",
                "text": "Message 3",
                "videoBytes": open("./video.png", "rb").read(),
            },
        ]
    )

    # Sending multiple WhatsApp messages in a batch
    whatsapp_sender = setup_whatsapp("http://your-whatsapp-api-endpoint")
    await whatsapp_sender(
        [
            {
                "chatId": "chat_id_1",
                "text": "Message 1",
            },
            {
                "chatId": "chat_id_2",
                "text": "Message 2",
                "imageBytes": open("./image.png", "rb").read(),
            },
            {
                "chatId": "chat_id_3",
                "text": "Message 3",
                "videoBytes": open("./video.png", "rb").read(),
            },
        ]
    )
```

## Configuration

You can customize the behavior of Galactic Messenger by setting the following environment variables:

- 📫 **EMAIL_SERVICE**: The email service provider. Choose "zoho" or "gmail". Default: "zoho".
- ⏳ **BATCH_TOTAL_TIMEOUT**: Total timeout in seconds for batch requests. Default: 30.
- ⏰ **BATCH_CONNECT_TIMEOUT**: Connection timeout in seconds for batch requests. Default: 5.
- ⏳ **SINGLE_TOTAL_TIMEOUT**: Total timeout in seconds for single requests. Default: 10.
- ⏰ **SINGLE_CONNECT_TIMEOUT**: Connection timeout in seconds for single requests. Default: 2.

## Contributing

Contributions to Galactic Messenger are welcome! If you find a bug, have a suggestion, or want to contribute code, please open an issue or submit a pull request on the [GitHub repository](https://github.com/your-username/galactic-messenger).
