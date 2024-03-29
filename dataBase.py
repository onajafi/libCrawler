#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import ast
import sqlite3
from datetime import datetime


def get_users_book_from_database():
    with sqlite3.connect("users.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        DB_table = cur.fetchall()
        print DB_table
        output_users = {}
        for elem in DB_table:
            output_users[elem[0]] = {"user": elem[5], "pass":elem[6], "state": None}
        return output_users

def check_STR(input):
    if input is None:
        return '-'
    return input

def _add_user_from_message(message):
    with sqlite3.connect("users.sqlite") as conn:
        conn.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?,?);",
                           (message.from_user.id,
                            check_STR(message.from_user.username),
                            check_STR(message.from_user.first_name),
                            check_STR(message.from_user.last_name),
                            datetime.now(),
                            None,
                            None))

def _check_the_user_in_DB(message):
    with sqlite3.connect("users.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE u_id=?",(message.from_user.id,))
        sample_test = cur.fetchone()
        if sample_test is not None:
            return True
        _add_user_from_message(message)
        return False

def _update_UserPass(userID,username_LIB,password_LIB):
    with sqlite3.connect("users.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET libUSR=?, libPASS=? WHERE u_id=?",
                    (username_LIB,password_LIB,userID))
        conn.commit()


#Delete in DB:
with sqlite3.connect("users.sqlite") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users("
                "u_id MEDIUMINT, "
                "u_name VARCHAR(100), "
                "u_first_name VARCHAR(100), "
                "u_last_name VARCHAR(100), "
                "u_time DATETIME, "
                "libUSR VARCHAR(100),"
                "libPASS VARCHAR(100));")

    conn.commit()






