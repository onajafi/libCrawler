#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from telebot import types
from emoji import emojize
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

none_markup = types.InlineKeyboardMarkup(row_width=1)

enter_userpass_markup = types.InlineKeyboardMarkup(row_width=1)
enter_userpass_markup.add(types.InlineKeyboardButton('ورود اطلاعات کاربری',callback_data='UserPass'))

simple_MAIN_markup = types.ReplyKeyboardMarkup()
simple_BTN_status = types.KeyboardButton(emojize('نمایش وضعیت امانات:bar_chart:', use_aliases=True))
simple_BTN_renew = types.KeyboardButton(emojize('تمدید فوری امانات:alarm_clock:', use_aliases=True))
simple_BTN_help = types.KeyboardButton(emojize('لیست دستورات:ledger:', use_aliases=True))
simple_MAIN_markup.row(simple_BTN_renew,simple_BTN_help)
simple_MAIN_markup.row(simple_BTN_status)


greetings = """سلام،
این بات برای خودکار سازی تمدید کتاب از کتابخانه‌های دانشگاه صنعتی شریف طراحی شده.
برای استفاده از این بات باید عضو کتابخانه دانشگاه صنعتی شریف باشید و نیز در library.sharif.ir حساب کاربری داشته باشید. در صورتی که کتابی را به امانت گرفته باشید این بات می‌تواند بصورت خودکار آن را برای شما تمدید کند و از دادن جریمه بابت تحویل دیر کتاب جلوگیری کند.
با وارد کردن اطلاعات کاربری، شما با <a href="https://github.com/onajafi/libCrawler/blob/master/termsAndConditions/temsAndCons.md/">شرایط و قوانین</a> استفاده از این بات موافقت کرده‌اید.

کدهای این بات، متن باز است که می‌توانید در لینک زیر به آنها دسترسی داشته باشید:
https://github.com/onajafi/libCrawler
"""

give_user = "نام کاربری را وارد کنید" \
            "(نام کاربری پیش‌فرض ایمیل می‌باشد):"

give_pass = "رمز را وارد کنید" \
            "(گذرواژه پیش‌فرض شماره دانشجویی می‌باشد):"

your_password_is_wrong = """رمز یا نام کاربری اشتباه می‌باشد.
مجددا اطلاعات کاربری را وارد کنید."""

trying_to_do_it = "در حال انجام عملیات...(2min)"

in_the_middle_of_a_process = "بات در حال پردازش دستور قبل است.\n حداکثر تا چند دقیقه دیگر آزاد می‌شود."

we_cant_do_it_now = "در حال حاضر، انجام عملیات امکان پذیر نمی‌باشد."

what_question_mark_v1 = "هان؟"
what_question_mark_v2 = "چی؟"

please_give_user_pass = "اطلاعات کاربری شما وارد نشده است. با زدن دکمه زیر آن را وارد کنید."

your_good_to_go = "اطلاعات کاربری شما ثبت شد. از این به بعد بات بطور روزانه فهرست امانت‌های شما را بررسی می‌کند و در صورت امکان، آنها را تمدید می‌کند."

getting_status = "در حال دریافت اطلاعات از سایت کتابخانه..."

tryin_to_renew = "در حال تمدید کتاب از سایت کتابخانه..."

error_in_getting_data = "خطا در دریافت اطلاعات از سایت"

cant_auto_renew = "خطا در تمدید خودکار کتاب...\n" \
                  "اگر برای چند روز متوالی این پیام را مشاهده کردین، یک بار دستی سایت کتاب خانه را بازدید کنید تا زمان تمدید را از دست ندهید!"

help_message = """
لیست دستورات
تمدید فوری امانات:
/renew
مشاهده لیست امانات:
/status
ارسال نظر ویا انتقاد:
/feedback
ارسال نام و رمز کارگری:
/enter_user_pass
"""

leave_your_message = "لطفا نظر ویا انتقادتان را ارسال کنید:\n" \
                     "(برای لغو عملیات از دستور /cancel استفاده کنید)"

feedBack_sent = "پیامتان ارسال شد :)"

canceled_successfully = "عملیات لغو شد"

