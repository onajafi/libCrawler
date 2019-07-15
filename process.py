#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from users import user_book
from inits import bot
import MSGs
from random import randrange

def process_user_call(call):
    user_ID = call.from_user.id
    call_TXT = call.data
    if(call_TXT == "UserPass"):
        user_book[user_ID]["state"] = "get_USER"
        bot.send_message(user_ID,MSGs.give_user)
    else:
        bot.send_message(user_ID, "خطا در دریافت دستور...")

def process_user_MSG(message):
    user_ID = message.chat.id
    msg_TXT = message.text
    if(user_book[user_ID]["state"] == "get_USER"):
        user_book[user_ID]["user"] = msg_TXT
        user_book[user_ID]["state"] = "get_PASS"
        bot.send_message(user_ID,MSGs.give_pass)

    elif(user_book[user_ID]["state"] == "get_PASS"):
        user_book[user_ID]["pass"] = msg_TXT
        user_book[user_ID]["state"] = None
        bot.send_message(user_ID,"Done")#TEST

    else:
        if(randrange(2) == 0):
            bot.send_message(user_ID,MSGs.what_question_mark_v1)
        else:
            bot.send_message(user_ID,MSGs.what_question_mark_v2)


def check_account_status(user_ID):
    pass
