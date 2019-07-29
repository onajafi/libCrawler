#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import datetime

import process
from inits import bot
import trafficController
import time, threading
import MSGs, users, Error_Handle
from emoji import emojize


#TODO add feedback
#TODO add respond
#TODO add the reply_markup_button

@bot.message_handler(commands=['start'])
@Error_Handle.secure_from_exception_MESSAGE
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id)
    if check == "OK":
        bot.send_message(message.chat.id,MSGs.greetings,reply_markup = MSGs.enter_userpass_markup,parse_mode='HTML')
        users.add_user(message)
        trafficController.drop_check(message.chat.id)

@bot.message_handler(commands=['enter_user_pass'])
@Error_Handle.secure_from_exception_MESSAGE
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id)
    if check == "OK":
        process.get_userpass(message.chat.id)
        trafficController.drop_check(message.chat.id)

@bot.message_handler(commands=['status'])
@Error_Handle.secure_from_exception_MESSAGE
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id)
    if check == "OK":
        process.check_account_status(message.chat.id)
        trafficController.drop_check(message.chat.id)

@bot.message_handler(commands=['renew'])
@Error_Handle.secure_from_exception_MESSAGE
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id)
    if check == "OK":
        process.renew_account_books(message.chat.id)
        trafficController.drop_check(message.chat.id)

@bot.message_handler(regexp="^"+emojize('لیست دستورات:ledger:', use_aliases=True)+"$")
@bot.message_handler(commands=['help'])
@Error_Handle.secure_from_exception_MESSAGE
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id)
    if check == "OK":
        process.send_help_MSG(message.chat.id)
        trafficController.drop_check(message.chat.id)

@bot.message_handler(commands=['feedback'])
@Error_Handle.secure_from_exception_MESSAGE
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id)
    if check == "OK":
        process.get_feedback(message.chat.id)
        trafficController.drop_check(message.chat.id)

@bot.message_handler(commands=['cancel'])
@Error_Handle.secure_from_exception_MESSAGE
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id)
    if check == "OK":
        process.cancel_action(message.chat.id)
        trafficController.drop_check(message.chat.id)

@bot.message_handler(content_types=['text'])
@Error_Handle.secure_from_exception_MESSAGE
def text_MSG(message):
    check = trafficController.check_spam(message.chat.id)
    if check == "OK":
        process.process_user_MSG(message)
        trafficController.drop_check(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
@Error_Handle.secure_from_exception_CALL
def test_callback(call):
    bot.answer_callback_query(call.id)

    if users.know_user(call.from_user.id) == False:
        return

    check = trafficController.check_spam(call.from_user.id)
    if check == "OK":
        process.process_user_call(call)
        trafficController.drop_check(call.from_user.id)





#Here are the threads:
RUN_THREAD = True
def MAIN_THR():
    global RUN_THREAD
    while(RUN_THREAD):
        try:
            bot.polling()
        except:
            pass
        time.sleep(2)

def RENEW_THR():
    global RUN_THREAD
    while(RUN_THREAD):
        try:
            now = datetime.datetime.utcnow() + datetime.timedelta(hours=3, minutes=30)
            ALARM_TIME = now + datetime.timedelta(days=1)
            ALARM_TIME = ALARM_TIME.replace(year=ALARM_TIME.year,
                                            month=ALARM_TIME.month,
                                            day=ALARM_TIME.day,
                                            hour=10, minute=00, second=00)
            wait_time = (ALARM_TIME - now).total_seconds() % (24 * 60 * 60)
            print "wait_time: ", wait_time
            # print (ALARM_TIME - now).total_seconds()
            time.sleep(wait_time)
            process.renew_all_users()

        except:
            pass
        time.sleep(2)

main_thread = threading.Thread(target = MAIN_THR)
renew_thread = threading.Thread(target = RENEW_THR)

main_thread.start()
renew_thread.start()

