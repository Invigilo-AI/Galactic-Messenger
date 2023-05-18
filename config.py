from typing import NamedTuple

Config = NamedTuple(
    "Config",
    [
        ("SMTP_SERVER", str),
        ("SINGLE_CONNECT_TIMEOUT", int),
        ("BATCH_CONNECT_TIMEOUT", int),
        ("SINGLE_TOTAL_TIMEOUT", int),
        ("BATCH_TOTAL_TIMEOUT", int),
    ],
)("ZOHO", 5, 5, 10, 60)
