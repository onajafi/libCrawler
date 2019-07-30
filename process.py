#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import json, time
import os, subprocess, signal
from random import randrange

import dataBase
import inits
from users import user_book
from inits import bot, feedBack_target_chat
import MSGs
import Error_Handle

dest_Chat_ID = -1

@Error_Handle.secure_from_exception_CALL
def process_user_call(call):
    user_ID = call.from_user.id
    call_TXT = call.data
    if(call_TXT == "UserPass"):
        user_book[user_ID]["state"] = "get_USER"
        bot.send_message(user_ID,MSGs.give_user)
    else:
        bot.send_message(user_ID, "خطا در دریافت دستور...")

@Error_Handle.secure_from_exception_MESSAGE
def process_user_MSG(message):
    global dest_Chat_ID
    user_ID = message.chat.id
    msg_TXT = message.text
    if(user_book[user_ID]["state"] == "get_USER"):
        user_book[user_ID]["user"] = msg_TXT
        user_book[user_ID]["state"] = "get_PASS"
        bot.send_message(user_ID,MSGs.give_pass)

    elif(user_book[user_ID]["state"] == "get_PASS"):
        user_book[user_ID]["pass"] = msg_TXT
        user_book[user_ID]["state"] = None
        check_account_status(user_ID)
        if (user_book[user_ID]["state"] == "DONE"):#Check if the user pass is OK and then bring in the database
            dataBase._update_UserPass(user_ID,user_book[user_ID]["user"],user_book[user_ID]["pass"])
            bot.send_message(user_ID, MSGs.your_good_to_go, reply_markup = MSGs.simple_MAIN_markup)
        else:
            user_book[user_ID]["user"] = None
            user_book[user_ID]["pass"] = None

    elif(user_book[user_ID]["state"] == "get_feedback"):
        bot.forward_message(feedBack_target_chat,user_ID,message.message_id)
        bot.send_message(feedBack_target_chat,"The users ID is:")
        bot.send_message(feedBack_target_chat,str(user_ID))
        bot.send_message(user_ID,MSGs.feedBack_sent, reply_markup = MSGs.simple_MAIN_markup)
        user_book[user_ID]["state"] = None

    elif(user_book[user_ID]["state"] == "admin_respond_get_chat_ID"):
        dest_Chat_ID = int(message.text)
        bot.send_message(feedBack_target_chat,"Leave response:")
        user_book[user_ID]["state"] = "admin_respond_entering_MSG"

    elif(user_book[user_ID]["state"] == "admin_respond_entering_MSG"):
        bot.send_message(dest_Chat_ID,message.text)
        bot.send_message(feedBack_target_chat,"Sent :)")
        dest_Chat_ID = -1

    else:
        if(randrange(2) == 0):
            bot.send_message(user_ID,MSGs.what_question_mark_v1)
        else:
            bot.send_message(user_ID,MSGs.what_question_mark_v2)

# This function doesn't renew the book!
# It just keeps you updated...
def check_account_status(user_ID,quiet=False):
    if(user_book[user_ID]["pass"] == None):
        bot.send_message(user_ID, MSGs.please_give_user_pass, reply_markup=MSGs.enter_userpass_markup)
        return
    if not quiet:
        bot.send_message(user_ID, MSGs.getting_status)

    input_data = {"pass": user_book[user_ID]["pass"],
                  "user": user_book[user_ID]["user"],
                  "chat_id": user_ID,
                  "extend":False}

    input_file_name = 'input_EXT_' + str(user_ID) + '.json'
    with open('tmp/' + input_file_name, 'w') as outfile:
        json.dump(input_data, outfile)

    try:
        p = subprocess.Popen(['casperjs',  'crawlers/EXT.js', input_file_name])
        print p.poll()
        for i in range(120):
            if (p.poll() is None):
                time.sleep(1)
    except:
        p.send_signal(signal.SIGINT)
        Error_Handle.log_error("SCRIPT ERROR: check_account_status")
        print "Script KILLED"
        return

    if (p.poll() is None):
        p.send_signal(signal.SIGINT)
        print "CTRL+C The script didn't get completely finished"
        bot.send_message(user_ID,MSGs.error_in_getting_data)
        return
    print "--DONE--"

    data = None
    data_output_file_name = 'output_EXT_' + str(user_ID) + '.json'
    # --Reading the results--
    with open('tmp/' + data_output_file_name) as f:
        data = json.load(f)

    # os.remove('tmp/' + data_output_file_name)
    # os.remove('tmp/' + input_file_name)

    if "ENTRY_STATE" not in data:
        bot.send_message(user_ID,MSGs.error_in_getting_data)
        return
    if data["ENTRY_STATE"] != "GOOD":
        bot.send_message(user_ID, MSGs.error_in_getting_data)
        return

    if data["PASSWORD_STATE"] == "WRONG":
        bot.send_message(user_ID, MSGs.your_password_is_wrong, reply_markup=MSGs.enter_userpass_markup)
        return


    main_MSG = ""
    for elem in data["table"]:
        temp_MSG = str(elem["rowNum"] + 1) + ".\n"
        temp_MSG += "عنوان کتاب:\n" + str(elem["title"]) + "\n"
        temp_MSG += "موعد بازگشت:\n" + str(elem["returnDate"]) + "\n"
        temp_MSG += "وضعیت:\n" + str(elem["status"]) + "\n"
        main_MSG += temp_MSG
        main_MSG += "-------------\n"

    bot.send_message(user_ID,main_MSG, reply_markup = MSGs.simple_MAIN_markup)

    user_book[user_ID]["state"] = "DONE"

# This function renews the book...
def renew_account_books(user_ID, quiet=False):
    if(user_book[user_ID]["pass"] == None):
        bot.send_message(user_ID, MSGs.please_give_user_pass, reply_markup=MSGs.enter_userpass_markup)
        return
    if not quiet:
        bot.send_message(user_ID, MSGs.tryin_to_renew)

    input_data = {"pass": user_book[user_ID]["pass"],
                  "user": user_book[user_ID]["user"],
                  "chat_id": user_ID,
                  "extend":True}

    input_file_name = 'input_EXT_' + str(user_ID) + '.json'
    with open('tmp/' + input_file_name, 'w') as outfile:
        json.dump(input_data, outfile)

    try:
        p = subprocess.Popen(['casperjs',  'crawlers/EXT.js', input_file_name])
        print p.poll()
        for i in range(120):
            if (p.poll() is None):
                time.sleep(1)
    except:
        p.send_signal(signal.SIGINT)
        Error_Handle.log_error("SCRIPT ERROR: check_account_status")
        print "Script KILLED"
        return

    if (p.poll() is None):
        p.send_signal(signal.SIGINT)
        print "CTRL+C The script didn't get completely finished"
        bot.send_message(user_ID,MSGs.error_in_getting_data)
        return
    print "--DONE--"

    data = None
    data_output_file_name = 'output_EXT_' + str(user_ID) + '.json'
    # --Reading the results--
    with open('tmp/' + data_output_file_name) as f:
        data = json.load(f)

    # os.remove('tmp/' + data_output_file_name)
    # os.remove('tmp/' + input_file_name)

    if "ENTRY_STATE" not in data:
        bot.send_message(user_ID,MSGs.error_in_getting_data)
        return
    if data["ENTRY_STATE"] != "GOOD":
        bot.send_message(user_ID, MSGs.error_in_getting_data)
        return

    if data["PASSWORD_STATE"] == "WRONG":
        bot.send_message(user_ID, MSGs.your_password_is_wrong, reply_markup=MSGs.enter_userpass_markup)
        return

    win_count = 0

    main_MSG = ""
    for elem in data["table"]:
        temp_MSG = str(elem["rowNum"] + 1) + ".\n"
        temp_MSG += "عنوان کتاب:\n" + str(elem["title"]) + "\n"
        temp_MSG += "موعد بازگشت:\n" + str(elem["returnDate"]) + "\n"
        temp_MSG += "وضعیت:\n" + str(elem["status"]) + "\n"
        main_MSG += temp_MSG
        main_MSG += "-------------\n"
        if(elem["extended_successfully"]):
            print "extended_successfully", elem["extended_successfully"]
            win_count += 1

    if ((not quiet) or (win_count > 0)):
        bot.send_message(user_ID, "تعداد کتاب‌های تمدید شده: " + str(win_count))
        bot.send_message(user_ID,main_MSG, reply_markup = MSGs.simple_MAIN_markup)

    user_book[user_ID]["state"] = "DONE"

def renew_all_users():
    count_win = 0
    count_loose = 0
    for user_ID in user_book.keys():
        try:
            if(user_book[user_ID]["user"] and user_book[user_ID]["pass"]):
                renew_account_books(user_ID, quiet=True)
                count_win+=1
            else:
                count_loose+=1
        except:
            try:
                bot.send_message(user_ID, MSGs.cant_auto_renew)
            except:
                pass# TODO Implement something to ignore the blockers
            Error_Handle.log_error("ERROR: " + "renew_all_users()::for")
            return
    bot.send_message(inits.feedBack_target_chat,
                     "Passed: " + str(count_win) + '\n'
                     "Failed: " + str(count_loose) + '\n'
                     "Total: " + str(count_win + count_loose)
                     )



if not os.path.exists('tmp'):
    os.makedirs('tmp')

def get_userpass(user_ID):
    user_book[user_ID]["state"] = "get_USER"
    bot.send_message(user_ID, MSGs.give_user)

def send_help_MSG(user_ID):
    bot.send_message(user_ID, MSGs.help_message, reply_markup = MSGs.simple_MAIN_markup)

def get_feedback(user_ID):
    user_book[user_ID]["state"] = "get_feedback"
    bot.send_message(user_ID, MSGs.leave_your_message)

def cancel_action(user_ID):
    user_book[user_ID]["state"] = None
    bot.send_message(user_ID, MSGs.canceled_successfully, reply_markup = MSGs.simple_MAIN_markup)

def respond_to_user_ID(user_ID):
    user_book[user_ID]["state"] = "admin_respond_get_chat_ID"
    bot.send_message(user_ID, "leave the destination chat ID:")


