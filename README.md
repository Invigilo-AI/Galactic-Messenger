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
    email_content = {
        "to": "recipient@example.com",
        "subject": "Hello",
        "message": "This is a test email.",
    }
    await email_sender(email_content)

    # Set up Telegram
    telegram_sender = setup_telegram("your_telegram_token")
    telegram_input = {
        "chatId": "your_chat_id",
        "text": "Hello from Galactic Messenger!",
    }
    await telegram_sender(telegram_input)

    # Set up WhatsApp
    whatsapp_sender = setup_whatsapp("http://your-whatsapp-api-endpoint")
    whatsapp_input = {
        "groupId": "your_group_id",
        "message": "Hello from Galactic Messenger!",
    }
    await whatsapp_sender(whatsapp_input)

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
# Sending multiple emails in a batch
email_content_1 = {
    "to": "recipient1@example.com",
    "subject": "Message 1",
    "message": "This is message 1.",
}
email_content_2 = {
    "to": "recipient2@example.com",
    "subject": "Message 2",
    "message": "This is message 2.",
}
email_contents = [email_content_1, email_content_2]
await email_sender(email_contents)

# Sending multiple Telegram messages in a batch
telegram_input_1 = {
    "chatId": "chat_id_1",
    "text": "Message 1",
}
telegram_input_2 = {
    "chatId": "chat_id_2",
    "text": "Message 2",
}
telegram_inputs = [telegram_input_1, telegram_input_2]
await telegram_sender(telegram_inputs)

# Sending multiple WhatsApp messages in a batch
whatsapp_input_1 = {
    "chatId": "group_id_1",
    "message": "Message 1",
}
whatsapp_input_2 = {
    "chatId": "group_id_2",
    "message": "Message 2",
}
whatsapp_inputs = [whatsapp_input_1, whatsapp_input_2]
await whatsapp_sender(whatsapp_inputs)
```

## Configuration

You

can customize the behavior of Galactic Messenger by setting the following environment variables:

- 📫 **EMAIL_SERVICE**: The email service provider. Choose "zoho" or "gmail". Default: "zoho".
- ⏳ **BATCH_TOTAL_TIMEOUT**: Total timeout in seconds for batch requests. Default: 30.
- ⏰ **BATCH_CONNECT_TIMEOUT**: Connection timeout in seconds for batch requests. Default: 5.
- ⏳ **SINGLE_TOTAL_TIMEOUT**: Total timeout in seconds for single requests. Default: 10.
- ⏰ **SINGLE_CONNECT_TIMEOUT**: Connection timeout in seconds for single requests. Default: 2.

## Contributing

Contributions to Galactic Messenger are welcome! If you find a bug, have a suggestion, or want to contribute code, please open an issue or submit a pull request on the [GitHub repository](https://github.com/your-username/galactic-messenger).
