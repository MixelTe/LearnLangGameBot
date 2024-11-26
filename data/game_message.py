from __future__ import annotations
from sqlalchemy import DateTime, Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy_serializer import SerializerMixin

from data.log import Actions, Log, Tables
from data.get_datetime_now import get_datetime_now
from data.user import User
import tgapi
from .db_session import SqlAlchemyBase


class GameMessage(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "GameMessage"

    created           = Column(DateTime, nullable=False)
    result_id         = Column(String(128), nullable=False)
    inline_message_id = Column(String(128), nullable=False)

    def __repr__(self):
        return f"<GameMessage> [{self.id} {self.inline_message_id}] {self.result_id}"

    @staticmethod
    def new(creator: User, result_id: str, inline_message_id: str):
        db_sess = Session.object_session(creator)
        now = get_datetime_now()
        message = GameMessage(result_id=result_id, inline_message_id=inline_message_id)
        message.created = now

        db_sess.add(message)
        Log.added(message, creator, Tables.GameMessage, [
            ("result_id", message.result_id),
            ("inline_message_id", message.inline_message_id),
        ], now)

        return message

    @staticmethod
    def new_from_data(creator: User, data: tgapi.ChosenInlineResult):
        return GameMessage.new(creator, data.result_id, data.inline_message_id)

    @staticmethod
    def get_by_inline_message_id(db_sess: Session, inline_message_id: str):
        return db_sess.query(GameMessage).filter(GameMessage.inline_message_id == inline_message_id).first()

    def get_dict(self):
        return {
            "id": self.id,
            "created": self.created,
            "result_id": self.result_id,
            "inline_message_id": self.inline_message_id,
        }
