from bot import process_update
from logger import set_logging
from flask import Flask, request

import tgapi


set_logging()
tgapi.setup()
app = Flask(__name__, static_folder=None)


def main():
    # if not os.path.exists("db"):
    #     os.makedirs("db")
    #     from scripts.init_values import init_values
    #     init_values(True)

    # db_session.global_init()

    # register_blueprints(app)
    if __name__ == "__main__":
        updates_listener()


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
    update_id = -1
    while True:
        ok, updates = tgapi.getUpdates(update_id + 1, 60)
        if not ok:
            break
        for update in updates:
            update_id = max(update_id, update.update_id)
            process_update(update)

main()
