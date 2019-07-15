#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from inits import bot
import Error_Handle, MSGs, dataBase

user_book = {}


def add_user(message):
    try:
        userID = message.chat.id
        if(userID not in user_book.keys()):
            user_book[userID] = {"user": None, "pass":None, "state":None}
            dataBase._check_the_user_in_DB(message)
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.add_user")
        return


def know_user(userID):
    try:
        if (userID not in user_book.keys()):
            return False
        return True
    except:
        Error_Handle.log_error("ERROR: users.know_user")
        return False


