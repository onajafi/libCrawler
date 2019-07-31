# LibCrawler
A web-crawler which renews your book reservation at [library.sharif.ir](http://library.sharif.ir).

## About
After a while of reserving books from our Universities library
 I found that the process of renewing your book reservation is pretty
much annoying! When you enter the website it is hard to see a login button!

![Website View](https://raw.githubusercontent.com/onajafi/libCrawler/master/_images/pic1_website.png)

But it's there some where...

![Renew button](https://raw.githubusercontent.com/onajafi/libCrawler/master/_images/pic2_renew.png)

After discovering and clicking that button, you have to login and find the page where the books can be renewed 
and click on the renewal button for each book (Nope, there is no "Renew All" button).

So I came up with the idea of writing this _Telegram Web Crawler_ bot.

Visit the bot at this address: [t.me/Lib_Crawler_Bot](https://t.me/Lib_Crawler_Bot)

## Setup
If you want to setup the bot on your own server follow these instructions.

This script was tested on Ubuntu 18.04
### NodeJS
If you don't have nodeJS installed, take a look at this link:

https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions

### PhantomJS & CasperJS

Checkout this link for setup instructions:

https://gist.github.com/onajafi/60499a2a7749fe4af4fa19d2b377bc08

### Telegram API python library

[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) is used to connect with the servers of Telegram, issue this commend to install it on your system:

```pip2 install pyTelegramBotAPI```

if you don't have pip installed, checkout [this link](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/#installing-pip-for-python-2).

### python emoji library

```pip2 install emoji```

### Clone the repo and initialize the script
Issue this command to get the script:

```git clone https://github.com/onajafi/libCrawler.git```

In Telegram create your bot using [BotFather](https://core.telegram.org/bots#6-botfather).

After getting your bots TOKEN, copy it and open 
the ```inits.py``` file, then paste the token 
instead of ```<###THE BOTS TOKEN###>``` ,
set the ```feedBack_target_chat``` variable a chat ID you like the feedbacks to be forwarded to,
otherwise, just write 0.
Chat IDs are integer numbers that are used to distinguish chats for the bot. You can find this number
 in the ```users.sqlite``` file after the bot has made a successful communication with a Telegram user.

Now you can run the script:

    cd libCrawler
    python libCrawler.py

Run the code on the back ground so it will keep running on the server while you're logged off:

    python libCrawler.py > /dev/null &








