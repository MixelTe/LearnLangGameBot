import logging
import os
from blueprints.register_blueprints import register_blueprints
from bot import process_update
from data import db_session
from logger import set_logging
from flask import Flask, abort, redirect, request, send_from_directory

import tgapi


set_logging()
tgapi.setup()
FRONTEND_FOLDER = "wwwroot"
app = Flask(__name__, static_folder=None)
is_local_run = __name__ == "__main__"


def main():
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
    logging.info(f"webhook: {request.json}")
    process_update(tgapi.Update(request.json))
    return "ok"


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def frontend(path: str):
    if request.path.startswith("/api"):
        abort(404)
    if path != "" and "." not in path and path[-1] != "/":
        qs = request.query_string.decode()
        if qs != "":
            qs = "?" + qs
        return redirect(f"/{path}/{qs}")
    if path.split("/")[-1] == "":
        path += "index.html"
    if not os.path.exists(FRONTEND_FOLDER + "/" + path):
        abort(404)

    res = send_from_directory(FRONTEND_FOLDER, path)
    if request.path.startswith("/static/"):
        res.headers.set("Cache-Control", f"public,max-age={60 * 60 * 24 * 14},immutable")
    else:
        if is_local_run:
            res.headers.set("Cache-Control", "no_cache")
        else:
            res.headers.set("Cache-Control", f"public,max-age={60 * 60}")
    return res


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
