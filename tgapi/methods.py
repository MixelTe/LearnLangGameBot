from .utils import call
from .types import *


def getUpdates(offset: int = 0, timeout: int = 0):
    ok, r = call("getUpdates", {"offset": offset, "timeout": timeout}, timeout=timeout+5)
    if not ok:
        return False, []
    return True, list(map(lambda x: Update(x), r["result"]))


def sendMessage(chat_id: str, text: str, message_thread_id: int = None, use_markdown = False):
    p = {
        "chat_id": chat_id,
        "message_thread_id": message_thread_id,
        "text": text,
    }
    if use_markdown:
        p["parse_mode"] = "MarkdownV2"
    ok, r = call("sendMessage", p)
    if not ok:
        return False, r
    return True, Message(r["result"])
