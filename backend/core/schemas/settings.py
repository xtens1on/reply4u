from pydantic import BaseModel


class AppSettingsSchema(BaseModel):
    system_message_template: str = ''
    message_template: str = ''
    model: str = ''
    users_active_by_default: bool = False


class UpdateAppSettingsSchema(BaseModel):
    system_message_template: str | None = None
    message_template: str | None = None
    model: str | None = None
    users_active_by_default: bool | None = None
