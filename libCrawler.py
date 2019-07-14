#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from inits import bot
import trafficController
import time, threading
import MSGs



@bot.message_handler(commands=['start'])
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id)
    if check == "OK":
        bot.send_message(message.chat.id,MSGs.greetings,reply_markup = MSGs.enter_userpass_markup,parse_mode='HTML')
        trafficController.drop_check(message.chat.id)




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

