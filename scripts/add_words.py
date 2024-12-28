import sys
import os


def add_words(dev=False, cmd=False):
    if cmd:
        add_parent_to_path()

    from data import db_session
    from data.theme import Theme
    from data.word import Word

    db_session.global_init(dev)
    db_sess = db_session.create_session()

    def add_theme(id_str, name, words):
        theme = Theme(id_str=id_str, name=name)
        db_sess.add(theme)
        db_sess.commit()
        for (trans, name) in words:
            if isinstance(trans, str):
                trans = [trans]
            db_sess.add(Word(name=name, trans=trans, themeId=theme.id))
        db_sess.commit()

    def init():
        add_theme("words", "Theme", [
            # (["", ""], ""),
            # ("", ""),
        ])

    init()


def add_parent_to_path():
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)


if __name__ == "__main__":
    add_words("dev" in sys.argv, True)