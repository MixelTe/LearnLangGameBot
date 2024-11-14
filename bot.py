import tgapi

def process_update(update: tgapi.Update):
    print(update)
    if update.inline_query is not None:
        onInlineQuery(update.inline_query)
    elif update.message and update.message.text != "":
        onMessage(update.message)
    elif update.callback_query is not None:
        onCallbackQuery(update.callback_query)


def onMessage(message: tgapi.Message):
    tgapi.sendMessage(message.chat.id, f"{message.text}")


def onInlineQuery(query: tgapi.InlineQuery):
    tgapi.answerInlineQuery(query.id, [
        tgapi.InlineQueryResultArticle("1", "Echo", tgapi.InputTextMessageContent(query.query or "Echo")),
        tgapi.InlineQueryResultArticle("2", "Шутка", tgapi.InputTextMessageContent('typeof NaN == "number"')),
        tgapi.InlineQueryResultGame("3", "words", tgapi.InlineKeyboardMarkup([[
            tgapi.InlineKeyboardButton.run_game(
                "Играть и выучить слова!" if query.sender.language_code == "ru" else "Play and learn words!"
                ),
        ]])),
    ], cache_time=1)


def onCallbackQuery(callback_query: tgapi.CallbackQuery):
    if callback_query.game_short_name == "words":
        tgapi.answerCallbackQuery(callback_query.id, url=f"https://example.com?uid={callback_query.sender.id}")
    else:
        tgapi.answerCallbackQuery(callback_query.id)
