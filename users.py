#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from inits import bot
import Error_Handle, MSGs, dataBase

user_book = dataBase.get_users_book_from_database()


def add_user(message):
    userID = message.chat.id
    if(userID not in user_book.keys()):
        user_book[userID] = {"user": None, "pass":None, "state":None}
        dataBase._check_the_user_in_DB(message)



def know_user(userID):
    try:
        if (userID not in user_book.keys()):
            return False
        return True
    except:
        Error_Handle.log_error("ERROR: users.know_user")
        return False


