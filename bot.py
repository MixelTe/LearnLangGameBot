from sqlalchemy.orm import Session

from data.user import User
import tgapi
from utils import use_db_session

def process_update(update: tgapi.Update):
    print(update)
    if update.inline_query is not None:
        onInlineQuery(update.inline_query)
    elif update.message and update.message.text != "":
        onMessage(update.message)
    elif update.callback_query is not None:
        onCallbackQuery(update.callback_query)


@use_db_session()
def onMessage(message: tgapi.Message, db_sess: Session):
    user = User.get_by_id_tg(db_sess, message.sender.id)
    if user is None:
        user = User.new_from_data(db_sess, message.sender)
    if user.is_admin:
        text = f"Hi! {user.first_name}\nDo you say: {message.text}?"
    else:
        text = "Мне не разрешают разговаривать с незнакомцами("
    tgapi.sendMessage(message.chat.id, text)


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
        tgapi.answerCallbackQuery(callback_query.id, url=tgapi.get_url(f"words/?uid={callback_query.sender.id}"))
    else:
        tgapi.answerCallbackQuery(callback_query.id)
