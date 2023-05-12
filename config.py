from typing import NamedTuple

Config = NamedTuple(
    "Config",
    [
        ("SMTP_SERVER", str),
        ("SMTP_PORT", int),
        ("SINGLE_CONNECT_TIMEOUT", int),
        ("BATCH_CONNECT_TIMEOUT", int),
        ("SINGLE_TOTAL_TIMEOUT", int),
        ("BATCH_TOTAL_TIMEOUT", int),
    ],
)("smtp.zoho.com", 587, 5, 5, 10, 60)
