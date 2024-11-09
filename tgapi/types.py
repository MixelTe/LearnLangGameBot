from typing import Any, Literal
from .utils import ParsedJson


class User(ParsedJson):
    # https://core.telegram.org/bots/api#user
    __id_field__ = "id"
    id: int = 0
    is_bot: bool = False
    first_name: str = ""
    last_name: str = ""
    username: str = ""
    language_code: str = ""


class Chat(ParsedJson):
    # https://core.telegram.org/bots/api#chat
    __id_field__ = "id"
    id: int = 0
    type: Literal["private", "group", "supergroup", "channel"] = ""
    title: str = ""
    is_forum: bool = False


class Message(ParsedJson):
    __id_field__ = "message_id"
    # https://core.telegram.org/bots/api#message
    message_id: int = 0
    sender: User = None
    chat: Chat = None
    text: str = ""
    date: int = 0

    def _parse_field(self, key: str, v: Any):
        if key == "from":
            return "sender", User(v)


class Update(ParsedJson):
    # https://core.telegram.org/bots/api#update
    __id_field__ = "update_id"
    update_id: int = 0
    message: Message = None
