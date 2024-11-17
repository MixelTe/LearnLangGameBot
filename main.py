from blueprints.register_blueprints import register_blueprints
from bot import process_update
from data import db_session
from logger import set_logging
from flask import Flask, request

import tgapi


set_logging()
tgapi.setup()
app = Flask(__name__, static_folder=None)


def main():
    is_local_run = __name__ == "__main__"

    db_session.global_init(file_db=is_local_run)

    register_blueprints(app)

    if is_local_run:
        runInBotMode = True
        if runInBotMode:
            updates_listener()
        else:
            app.run(debug=True, port=3000)


@app.route("/webhook", methods=["POST"])
def webhook():
    token = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if (not tgapi.check_webhook_token(token)):
        return "wrong token"
    process_update(tgapi.Update(request.json))
    return "ok"


@app.route("/")
def index():
    return "Hello world!"


def updates_listener():
    print("listening for updates...")
    update_id = -1
    while True:
        ok, updates = tgapi.getUpdates(update_id + 1, 60)
        if not ok:
            break
        for update in updates:
            update_id = max(update_id, update.update_id)
            process_update(update)

main()
