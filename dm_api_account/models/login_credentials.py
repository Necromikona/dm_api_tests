from pydantic import BaseModel, Field, ConfigDict


class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra="forbid")

    login: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")
    remember_me: bool = Field(..., description="Поле \"запомнить меня\"", alias="rememberMe")