from pydantic import BaseSettings, Field


class Env(BaseSettings):
    TEST_EMAIL: str = Field(..., min_length=1)
    TEST_PASSWORD: str = Field(..., min_length=1)
    TEST_DESTINATION_EMAIL: str = Field(..., min_length=1)
    TEST_WHATSAPP_IP: str = Field(..., min_length=1)
    TEST_WHATSAPP_GROUP_ID: str = Field(..., min_length=1)

    class Config:
        case_sensitive = True


env = Env(_env_file=".env")  # type: ignore
