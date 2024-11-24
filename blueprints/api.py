from flask import Blueprint, jsonify
# from sqlalchemy.orm import Session
# from utils import use_db_session, use_user
# from data.user import User


blueprint = Blueprint("api", __name__)


@blueprint.route("/api")
def api():
    return jsonify({"__desc__": "api of bot"}), 200

# @blueprint.route("/api/user")
# @use_db_session()
# @use_user()
# def user(db_sess: Session, user: User):
#     return jsonify(user.get_dict()), 200