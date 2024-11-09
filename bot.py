import tgapi

def process_update(update: tgapi.Update):
    print(update)
    if update.message.text == "":
        return
    tgapi.sendMessage(update.message.chat.id, f"{update.message.text}")
