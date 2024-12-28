from __future__ import annotations
from sqlalchemy import Column, ForeignKey, orm, Integer
from sqlalchemy.orm import Session
from sqlalchemy_serializer import SerializerMixin

from data.log import Log, Tables
from data.user import User
from .db_session import SqlAlchemyBase


class UserWord(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "UserWord"

    id = None
    userId = Column(Integer, ForeignKey("User.id"), primary_key=True, nullable=False)
    wordId = Column(Integer, ForeignKey("Word.id"), primary_key=True, nullable=False)
    tryies = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)

    user = orm.relationship("User")
    word = orm.relationship("Word")

    def __repr__(self):
        return f"<UserWord> [{self.id}] u{self.userId} w{self.wordId} {self.points}"

    @staticmethod
    def new(creator: User, userId: int, wordId: int, tryies: int, points: int):
        db_sess = Session.object_session(creator)
        user_word = UserWord(userId=userId, wordId=wordId, tryies=tryies, points=points)

        db_sess.add(user_word)
        Log.added(user_word, creator, Tables.UserWord, [
            ("userId", user_word.userId),
            ("wordId", user_word.wordId),
            ("tryies", user_word.tryies),
            ("points", user_word.points),
        ])

        return user_word

    def get_dict(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "wordId": self.wordId,
            "tryies": self.tryies,
            "points": self.points,
        }
