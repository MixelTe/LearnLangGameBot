from __future__ import annotations
from sqlalchemy import JSON, Column, ForeignKey, orm, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy_serializer import SerializerMixin

from data.log import Log, Tables
from data.user import User
from .db_session import SqlAlchemyBase


class Word(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "Word"

    name                     = Column(String(128), nullable=False)
    trans: Column[list[str]] = Column(JSON, nullable=False)
    themeId                  = Column(Integer, ForeignKey("Theme.id"), nullable=False)

    theme = orm.relationship("Theme")

    def __repr__(self):
        return f"<Word> [{self.id}] {self.name}"

    @staticmethod
    def new(creator: User, name: str, trans: list[str], themeId: str):
        db_sess = Session.object_session(creator)
        word = Word(name=name, trans=trans, themeId=themeId)

        db_sess.add(word)
        Log.added(word, creator, Tables.Word, [
            ("name", word.name),
            ("trans", word.trans),
            ("themeId", word.themeId),
        ])

        return word

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "trans": self.trans,
            "themeId": self.themeId,
        }
