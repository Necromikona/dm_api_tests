from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class GeneralError(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str = Field(..., description="Сообщение")