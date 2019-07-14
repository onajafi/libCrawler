##################################### Method 1
import mechanize
import cookielib
import time
import logging


my_time = time.time()

print "Starting:"


logging.basicConfig(filename='logs.log',level=logging.DEBUG)


# global VARS:
index1 = 0
WE_MADE_IT = False
answer_word = ""
list_of_delta=[]
#-----------
print "OMMGG"

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

# The site we will navigate into, handling it's session
br.open("http://library.sharif.ir/cas/login?renew=true&service=http://library.sharif.ir:80/parvan/j_spring_cas_security_check")
tmp_br = br
br.select_form(nr=0)
while(1):
    try:
        if(WE_MADE_IT):
            break
        if(index1 >=max):
            break

        br = tmp_br
        br.select_form(nr=0)

        # User credentials
        br.form['username'] = "onajafi141@gmail.com"
        br.form['password'] = "94105463"

        # -------------------unlocking-------------------

        delta = time.time()
        response = br.submit()
        delta = time.time() - delta

        print "Responses: ", response.get_data()
        print "Title(): ", response.get_title()
        list_of_delta.append(delta)

        if(len(response.geturl()) >= 40):
            print "new URL is:"
            print response.geturl()

            WE_MADE_IT = True
            break

    except Exception as e:
        logging.debug("Err in part1:")
        logging.debug(e.message)
        print "1-"
        print e.message
        break




logging.debug("DONE!!!!!!!!")

logging.debug("Process time: " + str(time.time() - my_time))
# expected_val=reduce(lambda x, y: x + y, list_of_delta) / len(list_of_delta)
# print "So far the average time delay is: " + str(expected_val)
# logging.debug("So far the average time delay is: " + str(expected_val))

print "DONE :)"
