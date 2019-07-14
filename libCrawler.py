#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import process
from inits import bot
import trafficController
import time, threading
import MSGs, users, Error_Handle



@bot.message_handler(commands=['start'])
@Error_Handle.secure_from_exception
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id)
    if check == "OK":
        bot.send_message(message.chat.id,MSGs.greetings,reply_markup = MSGs.enter_userpass_markup,parse_mode='HTML')
        trafficController.drop_check(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
@Error_Handle.secure_from_exception
def test_callback(call):
    bot.answer_callback_query(call.id)

    if users.know_user(call.from_user.id) == False:
        return

    check = trafficController.check_spam(call.from_user.id)
    if check == "OK":
        response = process.process_user_call(call)
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


main_thread = threading.Thread(target = MAIN_THR)

main_thread.start()

