from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async

from tg_bot import dispatcher
import tg_bot.modules.sql.userinfo_sql as sql


@run_async
def about_me(bot, update):
    message = update.effective_message
    is_reply = message.reply_to_message is not None
    if is_reply:
        user = message.reply_to_message.from_user
    else:
        user = message.from_user

    info = sql.get_user_me_info(user.id)

    if info:
        update.effective_message.reply_text("*{}*:\n{}".format(user.name, info),
                                            parse_mode=ParseMode.MARKDOWN)
    elif is_reply:
        username = message.reply_to_message.from_user.first_name
        update.effective_message.reply_text(username + " hasn't set an info message about himself yet!")
    else:
        update.effective_message.reply_text("You haven't set an info message about yourself yet!")


def set_about_me(bot, update):
    message = update.effective_message
    user_id = message.from_user.id
    text = message.text
    info = text.split(None, 1)  # use python's maxsplit to only remove the cmd, hence keeping newlines.
    if len(info) == 2:
        sql.set_user_me_info(user_id, info[1])
        update.effective_message.reply_text("Updated your info!")


def about_bio(bot, update):
    message = update.effective_message
    is_reply = message.reply_to_message is not None
    if is_reply:
        user = message.reply_to_message.from_user
    else:
        user = message.from_user

    info = sql.get_user_bio(user.id)

    if info:
        update.effective_message.reply_text("*{}*:\n{}".format(user.name, info),
                                            parse_mode=ParseMode.MARKDOWN)
    elif is_reply:
        username = message.reply_to_message.from_user.first_name
        update.effective_message.reply_text("{} hasn't had a message set for himselt yet!".format(username))
    else:
        update.effective_message.reply_text("You haven't had a bio set about yourself yet!")


def set_about_bio(bot, update):
    message = update.effective_message
    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id
        if user_id == message.from_user.id:
            message.reply_text("Ha, you can't set your own bio! You're at the mercy of others here...")
            return
        text = message.text
        bio = text.split(None, 1)  # use python's maxsplit to only remove the cmd, hence keeping newlines.
        if len(bio) == 2:
            sql.set_user_bio(user_id, bio[1])
            message.reply_text("Updated {}'s bio!".format(repl_message.from_user.name))

__help__ = """
 - /setbio <text>: while replying will save another user's bio
 - /bio: will get your or another user's bio
 - /setme <text>: will set your info
 - /me: will get your or another user's info
"""

SET_BIO_HANDLER = CommandHandler("setbio", set_about_bio)
GET_BIO_HANDLER = CommandHandler("bio", about_bio)

SET_ABOUT_HANDLER = CommandHandler("setme", set_about_me)
GET_ABOUT_HANDLER = CommandHandler("me", about_me)

dispatcher.add_handler(SET_BIO_HANDLER)
dispatcher.add_handler(GET_BIO_HANDLER)
dispatcher.add_handler(SET_ABOUT_HANDLER)
dispatcher.add_handler(GET_ABOUT_HANDLER)