#!/usr/bin/python
import os
import time, schedule
from random import randint
import MySQLdb as mdb
import requests
from slackclient import SlackClient
from default import DATABASE_DEFAULT, BOT_TOKEN


# starterbot's ID as an environment variable
BOT_ID = BOT_TOKEN['bot_user_id']
SLACK_BOT_TOKEN = BOT_TOKEN['bot_access_token']

USER_MAPPING = {}
NUMBER_MENTIONS = 5 #sending 5 mentions per batch

COUNT_MENTIONS = 0
#Introductions phrases

PHRASES = [
    "Annotate a mention, and save a puppy 🐶",
    "A mention a day keeps the fat away 🍔",
    "Magneto requires humans to annotate mentions for the mutants 🤖",
    "Hello there! Here is your order 😘",
    "How dare you forget me! Here is your punishment 😈",
]

BLACK_LIST = [
    'adriana',
    'andrewbrennan',
    'patrick',
    'joei'
]

# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)

msql = mdb.connect(
            host=DATABASE_DEFAULT['host_db'],
            user=DATABASE_DEFAULT['user_db'],
            passwd=DATABASE_DEFAULT['password_db'],
            db=DATABASE_DEFAULT['name_db'])

def generate_message():
       return {
            "text": "This is my mention",
            "fallback": "A new mention to annotate 😘",
            "callback_id": "mention_id",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "footer": "url",
            "actions": [
                {
                    "name": "positive",
                    "text": "Positive 👍",
                    "type": "button",
                    "value": "1",
                    "style": "primary",
                },
                {
                    "name": "neutral",
                    "text": "Neutral 😐",
                    "type": "button",
                    "value": "0"
                },
                {
                    "name": "negative",
                    "text": "Negative 👎",
                    "type": "button",
                    "style": "danger",
                    "color": "#E35454",
                    "value": "-1",                 
                },
                {
                    "name": "idk",
                    "text": "I don't know 🤔",
                    "type": "button",
                    "value": "2",
                }
            ]
        }

def generate_template():
    return {
        "text": "intro text",
        "attachments": []
    }


def getCursor(query, msql=msql, params=None):
    try:
        cursor = msql.cursor()
        cursor.execute(query) if not params else cursor.execute(query, params)
    except Exception as e:
        cursor = msql.cursor()
        cursor.execute(query) if not params else cursor.execute(query, params)
    msql.commit()
    return cursor

def size_db():
    query = """SELECT COUNT(*) FROM Annotations"""
    cursor = getCursor(query)
    result=cursor.fetchone()
    return result[0]

def extractMention():
    count = size_db()
    print('size db: ',count)
    query = """SELECT mention_id, text, sourceUrl
        FROM Annotations LIMIT 1 OFFSET %s"""%randint(1,count)
    
    cursor = getCursor(query)
    numrows = int(cursor.rowcount)

    if numrows == 0:
        raise ValueError("No more mention to annotate")
    
    result = cursor.fetchone()
    cursor.close()
    return {'mention_id':result[0],
            'text': result[1],
            'url': result[2]}

def add_user_in_db(name):
    query = """INSERT IGNORE INTO Score (name) VALUES (%s)"""
    print(query)
    cursor = getCursor(query, params=(name,))
    cursor.close()

def check_if_new_users():
    """
    Check if a new user was added on Slack
    """
    try:
        userlist = slack_client.api_call("users.list")
        if 'members' in userlist.keys():
            user_list = userlist['members']
            if len(user_list) != len(USER_MAPPING):
                for user in user_list:
                    #to only list european users
                    if user.get('tz'):
                        if "Europe" in user['tz'] and not user['deleted']:
                            add_user_in_db(user['name'])
                            print('Inserted new member', user['name'])
                            USER_MAPPING[user['name']] = user['id']
        else:
            raise Exception("Couldn't fetch members list")
    except:
        raise Exception('Failed to check if new users')


def send_messages_to_users():
    #updating mapping of users
    msql.ping(True)
    check_if_new_users()

    COUNT_MENTIONS = size_db()
    BATCH = 0
    for k,v in USER_MAPPING.items():
        if k not in BLACK_LIST:
            if BATCH == 5:
                time.sleep(300)
            hello = giphy_hello()
            intro = PHRASES[randint(0,len(PHRASES)-1)] + " " + hello
            slack_client.api_call("chat.postMessage",channel=v,text=intro, as_user=True)
            for i in range(NUMBER_MENTIONS):
                mention = extractMention()
                l = generate_message()
                l['text'] = mention['text']
                l['footer'] = mention['url']
                l['callback_id'] = mention['mention_id']
                slack_client.api_call("chat.postMessage",channel=v,text="",attachments=[l], as_user=True)
                time.sleep(1)

            gif = giphy_thank_you()
            slack_client.api_call("chat.postMessage",channel=v,text=gif, as_user=True)

            BATCH += 1

def send_rankings():
    query = """SELECT (name, score) FROM Score"""
    cursor = getCursor(query)
    results = cursor.fetchall()
    return results

def giphy_thank_you():
    try:
        r = requests.get("http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=thank+you").json()
        return r['data']['url']
    except:
        return ""

def giphy_hello():
    try:
        r = requests.get("http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag=hello").json()
        return r['data']['url']
    except:
        return ""

def send_start_up_message():
    try:
        t = time.time()
        s = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        message = "Sentiment bot started at: %s" %s
        slack_client.api_call("chat.postMessage",channel="testbot", text=message)
    except:
        raise Exception("Failed to send startup messane and communicate with Slack API")

if __name__ == '__main__':
    print("SentimentBot called!")
    send_start_up_message()

    #loading user mapping
    check_if_new_users()
    print("User mapping: ", USER_MAPPING)

    #scheduling
    schedule.every().monday.at("13:45").do(send_messages_to_users)
    schedule.every().tuesday.at("14:00").do(send_messages_to_users)
    schedule.every().wednesday.at("15:15").do(send_messages_to_users)
    schedule.every().thursday.at("14:30").do(send_messages_to_users)
    schedule.every().friday.at("15:00").do(send_messages_to_users)
    print("Scheduling done, running...")

    while True:
        schedule.run_pending()
        time.sleep(1)
