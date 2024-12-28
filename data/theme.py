from __future__ import annotations
from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from sqlalchemy_serializer import SerializerMixin

from data.log import Log, Tables
from data.user import User
from .db_session import SqlAlchemyBase


class Theme(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "Theme"

    name   = Column(String(128), nullable=False)
    id_str = Column(String(128), nullable=False)

    def __repr__(self):
        return f"<Theme> [{self.id} {self.id_str}] {self.name}"

    @staticmethod
    def new(creator: User, id_str: str, name: str):
        db_sess = Session.object_session(creator)
        theme = Theme(id_str=id_str, name=name)

        db_sess.add(theme)
        Log.added(theme, creator, Tables.Theme, [
            ("name", theme.name),
            ("id_str", theme.id_str),
        ])

        return theme

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_str": self.id_str,
        }
