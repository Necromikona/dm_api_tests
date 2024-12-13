from __future__ import annotations

from dm_api_account.models.user_envelope import User
from enum import Enum
from typing import (
    Literal,
    Optional,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)

class ColorSchema(str, Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSICPALE = "ClassicPale"
    NIGHT = "Night"

class BbParseMode(str, Enum):
    COMMON = "Common"
    INFO = "Info"
    POST = "Post"
    CHAT = "Chat"

class InfoBbText(BaseModel):
    value: str = Field(None, alias='value')
    parse_mode: BbParseMode

class PagingSettings(BaseModel):
    posts_per_page: int = Field(..., alias='postsPerPage')
    comments_per_page: int = Field(..., alias='commentsPerPage')
    topics_per_page: int = Field(..., alias='topicsPerPage')
    messages_per_page: int = Field(..., alias='messagesPerPage')
    entities_per_page: int = Field(..., alias='entitiesPerPage')


class UserSettings(BaseModel):
    color_schema: ColorSchema = Field(None, alias='colorSchema')
    nanny_greetings_message: str = Field(None, alias='nannyGreetingsMessage')
    paging: PagingSettings


class UserDetails(User):
    icq: str = Field(None, alias='icq')
    skype: str = Field(None, alias='skype')
    original_picture_url: str = Field(None, alias='originalPictureUrl')
    info: Union[InfoBbText,Literal[""]]  = None
    settings:  Optional[UserSettings]  = None

class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None
