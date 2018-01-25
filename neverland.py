#!/usr/bin/env/python3

import requests
import bs4
from twilio.rest import Client
# import smtplib
import os

site = requests.get("https://mangastream.com/")
site.raise_for_status()


mstream_soup = bs4.BeautifulSoup(site.text, "lxml")

links = mstream_soup.find_all("a")

neverland = []

for link in links:
    if "neverland" in link.get("href"):
        neverland.append(link)


if "Today" in str(neverland):
    if os.path.isfile("/home/Matt/scripts/test.txt"):
        quit()
    else:
        accountSID = "AC09ab7be7155048435f6fa085e6e16a1e"
        authToken = "03f422196dcdcd253e238336eedbf1a7"
        twilioCli = Client(accountSID, authToken)
        tnum = "+12342319880"
        mynum = "+5519991300204"
        message = twilioCli.messages.create(from_ = tnum,
                                                to = mynum,
                                                body = "A new Promised Neverland Chapter is out!")
        with open("test.txt", "w") as f:
            f
else:
    if os.path.isfile("/home/Matt/scripts/test.txt"):
        os.remove("/home/Matt/scripts/test.txt")

# if "Today" in str(neverland):
#    mail = smtplib.SMTP("smtp.gmail.com",587)
#    mail.ehlo()
#   mail.starttls()
#   mail.login(user = "mbfiamenghi@gmail.com", password = "Mbf$cotland")
#    mail.sendmail("mbfiamenghi@gmail.com", "mbfiamenghi@gmail.com",
#              "Subject: New Promised Neverland Chapter.\nA new chapter of Promised Neverland is out!")
#    mail.quit()
