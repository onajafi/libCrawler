#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from datetime import datetime
from inits import bot
import MSGs

# Dictionary format-> userID:(type,time)
last_user_msg_time = {}


#This function will check if a user is
# using the proper amount of load on the server
## returns "SPAM" if it's a spam (not implemented)
## "IGNORE" if there is no need to take any action
## "IN_PROC" tell that where in a process right now
## "OK" if everything is cool
def check_spam(userID):
    if userID in last_user_msg_time.keys():
        print "traffic_controller:",last_user_msg_time[userID]
        if(datetime.now() - last_user_msg_time[userID]).total_seconds() < 130:
            bot.send_message(userID,
                             MSGs.in_the_middle_of_a_process)
            return "IN_PROC"
        else:
            print "traffic_controller:","IGNORING"
            return "IGNORE"

    last_user_msg_time[userID] = datetime.now()
    return "OK"

def finished_process(userID):
    if userID in last_user_msg_time.keys():
        del last_user_msg_time[userID]
        print "traffic_controller: PROCESS FINISHED"

def drop_check(userID):
    if userID in last_user_msg_time.keys():
        del last_user_msg_time[userID]



