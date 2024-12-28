from random import choices
from flask import Blueprint, jsonify
from sqlalchemy.orm import Session
from data.theme import Theme
from data.word import Word
from utils import get_json_values_from_req, response_not_found, use_db_session
from data.user import User


blueprint = Blueprint("api", __name__)


@blueprint.route("/api")
def api():
    return jsonify({"__desc__": "api of bot"}), 200


@blueprint.route("/api/get_words", methods=["POST"])
@use_db_session()
def get_words(db_sess: Session):
    uid, tid = get_json_values_from_req("uid", "tid")

    theme = Theme.get(db_sess, tid)
    if not theme:
        return response_not_found("theme", tid)

    words = db_sess.query(Word).filter(Word.themeId == theme.id).all()
    words = choices(words, k=5)
    data = {
        "title": theme.name,
        "questions": list(map(lambda w: {
                "type": "WordInput",
                "id": w.id,
                "question": w.name,
                "answers": w.trans,
			}, words)),
    }
    return jsonify(data), 200


@blueprint.route("/api/save_result", methods=["POST"])
@use_db_session()
def save_result(db_sess: Session):
    uid, results = get_json_values_from_req("uid", "results")

    data = {
        "score": 111,
    }

    return jsonify(data), 200
