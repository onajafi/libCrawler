#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import traceback

import trafficController
from inits import bot
import MSGs

f = open('error.txt', 'w+')
f.close()

def log_error(title):
    try:
        f = open('error.txt', 'a')
        f.write("\n\n\n" + str(title) + "-------------------\n")
        traceback.print_exc(file=f)
        f.close()
    except:
        print "Error in log() error handler :/"


# This is a function decorator to keep it from killing the hole bot when giving an error
def secure_from_exception_no_args(FUNC):
    def output_FUNC():
        try:
            FUNC()
        except:
            log_error("ERROR: " + FUNC.__name__)
            return
    return output_FUNC

# The Function (FUNC) has only 1 argument which is the userID
def secure_from_exception(FUNC):
    def output_FUNC(input_userID):
        try:
            FUNC(input_userID)
        except:
            bot.send_message(input_userID,MSGs.we_cant_do_it_now)
            trafficController.drop_check(input_userID)
            log_error("ERROR: " + FUNC.__name__)
            return
    return output_FUNC

def secure_from_exception_MESSAGE(FUNC):
    def output_FUNC(input_message):
        try:
            FUNC(input_message)
        except:
            bot.send_message(input_message.chat.id,MSGs.we_cant_do_it_now)
            trafficController.drop_check(input_message.chat.id)
            log_error("ERROR: " + FUNC.__name__)
            return
    return output_FUNC

def secure_from_exception_CALL(FUNC):
    def output_FUNC(input_call):
        try:
            FUNC(input_call)
        except:
            bot.send_message(input_call.from_user.id,MSGs.we_cant_do_it_now)
            trafficController.drop_check(input_call.from_user.id)
            log_error("ERROR: " + FUNC.__name__)
            return
    return output_FUNC

def secure_from_exception_2input(FUNC):
    def output_FUNC(input_userID,input_2nd):
        try:
            FUNC(input_userID,input_2nd)
        except:
            bot.send_message(input_userID,MSGs.we_cant_do_it_now)
            trafficController.drop_check(input_userID)
            log_error("ERROR: " + FUNC.__name__)
            return
    return output_FUNC

