from sqlalchemy.orm import Session

from data.game_message import GameMessage
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
    elif update.chosen_inline_result is not None:
        onChosenInlineResult(update.chosen_inline_result)


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


THEMES = [("3.1.1", "Theme 3.1.1"), ("3.1.2", "Theme 3.1.2"), ("3.3", "Theme 3.3"), ("4.1", "Theme 4.1"), ]
def onInlineQuery(query: tgapi.InlineQuery):
    txt = "Играть и выучить слова!" if query.sender.language_code == "ru" else "Play and learn words!"
    txt2 = "Ничего не найдено" if query.sender.language_code == "ru" else "Nothing was found"
    qt = query.query.strip().lower()
    word_games = [v for v in THEMES if v[0].startswith(qt)]
    if len(word_games) == 1:
        tgapi.answerInlineQuery(query.id, [
            tgapi.InlineQueryResultGame("game_" + v[0], "words", tgapi.InlineKeyboardMarkup([[
                    tgapi.InlineKeyboardButton.run_game(txt)
                ]])) for v in word_games
            ], cache_time=1)
    elif len(word_games) == 0:
        tgapi.answerInlineQuery(query.id, [
            tgapi.InlineQueryResultArticle("hint_no", txt2, tgapi.InputTextMessageContent("400"))
            ], cache_time=1)
    else:
        tgapi.answerInlineQuery(query.id, [
            tgapi.InlineQueryResultArticle("hint_" + v[0], v[1], tgapi.InputTextMessageContent("400")
                                           ) for v in word_games
            ], cache_time=1)


@use_db_session()
def onCallbackQuery(callback_query: tgapi.CallbackQuery, db_sess: Session):
    msg = GameMessage.get_by_inline_message_id(db_sess, callback_query.inline_message_id)
    if msg is None:
        txt = "Эта кнопка не работает!" if callback_query.sender.language_code == "ru" else "This button don't work!"
        tgapi.answerCallbackQuery(callback_query.id, txt)
        return
    url = f"words/?uid={callback_query.sender.id}&id={msg.result_id}"
    tgapi.answerCallbackQuery(callback_query.id, url=tgapi.get_url(url))


@use_db_session()
def onChosenInlineResult(chosen_inline_result: tgapi.ChosenInlineResult, db_sess: Session):
    if chosen_inline_result.result_id.startswith("game_"):
        GameMessage.new_from_data(User.get_admin(db_sess), chosen_inline_result)
