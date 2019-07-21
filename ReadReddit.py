"""
Title: Computer Part Updater
Author: Chidi Ewenike
Date: 07/21/2019
Description:

"""

import requests
import json
import time
import smtplib
from twilio.rest import Client
import sys

limit = sys.argv[1]
jsonPath = sys.argv[2]

link = "https://www.reddit.com/r/hardwareswap/new.json?sort=new&limit=" + str(limit)
agent = {'User-agent': 'HWBot'}
wanted={'2080','curve','144','2080ti','144hz','kraken','[usa-ca]'}

read = {}
info = {}

with open(jsonPath, "r") as jsonInfo:
    info = json.load(jsonInfo) 


def sendMsg(title, body, url):
    account_sid = info["sid"]
    auth_token = info["token"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                     body="Posting: " + title + "\nURL: " + url +  "\n\nDescription: " + body + "\n",
                     from_=info["from"],
                     to=info["to"])
'''
carriers = {
    'att':    '@txt.att.net',
    'tmobile':' @tmomail.net',
    'verizon':  '@vtext.com',
    'sprint':   '@page.nextel.com'
}

def sendMsg(title, body):
        # Replace the number with your own, or consider using an argument\dict for multiple people.
    to_number = '5622742608{}'.format(carriers['att'])
    auth = ('6971jec@gmail.com', 'juhani92')

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login(auth[0], auth[1])
    message = "Posting: " + title + "\nDescription: " + body + "\n"
    # Send text message through SMS gateway of destination number
    server.sendmail( auth[0], to_number, message)
'''
while(True):
    print("Session Starting %s" % time.strftime("%m-%d %H:%M:%S"))
    jsonData = requests.get(link, headers=agent)
    data = json.loads(jsonData.text)
    posts = data['data']['children']

    with open("read.json", "r") as rData:
        read = json.load(rData)

    oldCount = 0
    newCount = 0
    for text in posts:
        for word in text['data']['title'].split():
            for want in wanted:
                if want in word.lower():
                    if (text['data']['title'] not in read): 
                        #print(word.lower())
                        read[text['data']['title']] = 0
                        sendMsg(text['data']['title'], text['data']['selftext'][:1500-(len(text['data']['title']) + len(text['data']['url']))], text['data']['url']) 
                        print("\nPosting Found:\n\n")
                        print(text['data']['title'])
                        print("=====================================================================================================================\n")
                        print(text['data']['selftext'])
                        print("=====================================================================================================================\n\n")
                        newCount += 1
                    else:
                        oldCount += 1

    print("\nNumber of old postings in current session: %d\n\nNumber of new postings in current sessions: %d\n\n" % (oldCount, newCount))

    with open("read.json", "w") as wrData:    
        json.dump(read, wrData)

    time.sleep(60)

