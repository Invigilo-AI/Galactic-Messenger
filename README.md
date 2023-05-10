# Alert Service 🚀

The **Alert Service** is a Python package that provides a simple lightweight client for sending out messages to **Telegram** 📱, **Whatsapp** 📞, and **Email** 📧. It offers various methods for sending messages, images, and videos to different messaging platforms.

## Installation ⚙️

To install the Alert Service package, you can use pip:

```shell
pip install alert-service
```

## Usage 📝

### Initialization 🚀

To use the Alert Service, you need to initialize an instance of the `Alert` class with the desired messaging service and a token. The supported messaging services are **Whatsapp**, **Telegram**, and **Email**. The token is a required parameter and represents the authentication token or IP address for the corresponding service.

```python
from alert_service import Alert, Service

# Initialize the Alert Service with Whatsapp
whatsapp_alert = Alert(Service.WHATSAPP, "YOUR_WHATSAPP_TOKEN")

# Initialize the Alert Service with Telegram
telegram_alert = Alert(Service.TELEGRAM, "YOUR_TELEGRAM_TOKEN")

# Initialize the Alert Service with Email
email_alert = Alert(Service.EMAIL, "YOUR_EMAIL_TOKEN")
```

### Sending Messages ✉️

The Alert Service provides methods for sending messages to the selected messaging service.

```python
# Send a message
whatsapp_alert.send_one_message("TO_PHONE_NUMBER", {"message": "Hello, World! 👋"})

# Send an image
telegram_alert.send_one_image("TO_CHAT_ID", {"caption": "Image 📷", "image_bytes": b"IMAGE_BYTES"})

# Send a video
email_alert.send_one_video("TO_EMAIL_ADDRESS", {"caption": "Video 🎥", "video_bytes": b"VIDEO_BYTES"})
```

### Customization and Extensibility 🎨

The Alert Service is designed to be extensible and customizable. You can add support for additional messaging services by creating new classes that implement the required methods and interfaces. The `Alert` class acts as a mediator between the messaging service clients and provides a unified interface for sending messages.

## Configuration ⚙️

The Alert Service allows you to configure various timeouts for connecting and sending requests. The default timeout values are as follows:

- Single Connect Timeout: 5 seconds ⏱️
- Batch Connect Timeout: 5 seconds ⏱️
- Single Total Timeout: 10 seconds ⏱️
- Batch Total Timeout: 60 seconds ⏱️

If you need to customize these timeouts, you can modify the `Config` enum values accordingly.

## Examples 🌟

Here are some examples demonstrating the usage of the Alert Service:

```python
from alert_service import Alert, Service

# Initialize the Alert Service with Whatsapp
whatsapp_alert = Alert(Service.WHATSAPP, "YOUR_WHATSAPP_TOKEN")

# Send a message
whatsapp_alert.send_one_message("TO_PHONE_NUMBER", {"message": "Hello, World! 👋"})

# Send an image
whatsapp_alert.send_one_image("TO_PHONE_NUMBER", {"caption": "Image 📷", "image_bytes": b"IMAGE_BYTES"})

# Send a video
whatsapp_alert.send_one_video("TO_PHONE_NUMBER", {"caption": "Video 🎥", "video_bytes": b"VIDEO_BYTES"})


# Initialize the Alert Service with Telegram
telegram_alert = Alert(Service.TELEGRAM, "YOUR_TELEGRAM_TOKEN")

# Send a message
telegram_alert.send_one_message("TO_CHAT_ID", {"message": "Hello, World! 👋"})

# Send an image
telegram_alert.send_one_image("TO_CHAT_ID", {"caption": "Image 📷", "image_bytes": b"IMAGE_BYTES"})

# Send a video
telegram_alert.send_one_video("TO_CHAT_ID", {"caption": "Video 🎥", "video_bytes": b"VIDEO_BYTES"})


# Initialize the Alert Service with Email
email_alert = Alert(Service.EMAIL, "YOUR_EMAIL_TOKEN")

# Send a message
email_alert.send_one_message("TO_EMAIL_ADDRESS", {"message": "Hello, World! 👋"})

# Send an image
email_alert.send_one_image("TO_EMAIL_ADDRESS", {"caption": "Image 📷", "image_bytes": b"IMAGE_BYTES"})

# Send a video
email_alert.send_one_video("TO_EMAIL_ADDRESS", {"caption": "Video 🎥", "video_bytes": b"VIDEO_BYTES"})
```

## Conclusion 🎉

The Alert Service provides a convenient and efficient way to send messages, images, and videos to popular messaging platforms such as Whatsapp, Telegram, and Email. With its simple interface and extensibility, you can easily integrate it into your projects and enhance your notification capabilities.

Give it a try and start alerting your users and stakeholders with ease! If you encounter any issues or have suggestions for improvement, feel free to reach out to the Alert Service community or open an issue on the project repository.

Happy alerting! 🚀✉️📷🎥📧
