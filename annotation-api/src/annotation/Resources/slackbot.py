import MySQLdb as mdb
import json
from random import randint
from flask import request
from flask_restful import Resource, reqparse
from annotation.config.default import VERIFICATION_TOKEN

CONGRATS = [
    "Boom one puppy saved! 👏",
    "Mention got better! 👊",
    "Yeah again pleaaase!",
    "Well done mate!",
    "Thank you my dear 🙏",
    "What a nice person you are 😘",
    "Give me your phone number cutty 😳",
    "Congratulations, you are a rockstar!",
]


parser = reqparse.RequestParser()

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
        "text": "Annotate a mention, and save a puppy 🐶",
        "attachments": []
    }

message_error = {
    "text": "Oops incorrect input 🤗"
}

message_too_big = {
    "text": "You are a little greedy boy!😡 A smaller sample is wiser young padawan 🙄"
}

def verify_token(token):
    return VERIFICATION_TOKEN == token

class SlackbotSendMention(Resource):

    def __init__(self, **kwargs):
        self.config = kwargs['config']
        
        self.host_db = self.config['host_db']
        self.user_db = self.config['user_db']
        self.password_db = self.config['password_db']
        self.name_db = self.config['name_db']

        self.connectDb()
        self.size_db()

    def connectDb(self):
        self.db = mdb.connect(
            host=self.host_db,
            user=self.user_db,
            passwd=self.password_db,
            db=self.name_db)

    def getCursor(self, query):
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
        except Exception as e:
            self.connectDb()
            cursor = self.db.cursor()
            cursor.execute(query)
        self.db.commit()
        return cursor

    def size_db(self):
        query = """SELECT COUNT(*) FROM Annotations"""
        cursor = self.getCursor(query)
        result=cursor.fetchone()
        self.count = result[0]

    def extractMention(self):
        query = """SELECT mention_id, text, sourceUrl
            FROM Annotations LIMIT 1 OFFSET %s"""%randint(1,self.count)
        
        cursor = self.getCursor(query)
        numrows = int(cursor.rowcount)

        if numrows == 0:
            raise ValueError("No more mention to annotate")
        
        result = cursor.fetchone()
        cursor.close()
        return {'mention_id':result[0],
                'text': result[1],
                'url': result[2]}

    def post(self):
        try:
            parser.add_argument('text', location='form')
            parser.add_argument('token')
            args = parser.parse_args()
            if not verify_token(args['token']):
                return {
                    'error': 'Unauthorized access, GTFO'
                }
            if args['text'].isdigit():
                args = json.loads(args['text'])
            elif len(args['text']) == 0:
                args = 1
            if not isinstance(args, int):
                return message_error, 200
            elif args > 10:
                return message_too_big, 200
            else:
                response = generate_template()
                for i in range(args):
                    res = self.extractMention()
                    message = generate_message()
                    message['text'] = res['text']
                    message['callback_id'] = str(res['mention_id'])
                    message['footer'] = res['url']
                    response['attachments'].append(message)
                return response, 200
        except Exception as e:
            return {
                'status': 'error',
                'error': repr(e)}

class SlackbotButtonAction(Resource):

    def __init__(self, **kwargs):
        self.config = kwargs['config']
        
        self.host_db = self.config['host_db']
        self.user_db = self.config['user_db']
        self.password_db = self.config['password_db']
        self.name_db = self.config['name_db']

        self.connectDb()

    def connectDb(self):
        self.db = mdb.connect(
            host=self.host_db,
            user=self.user_db,
            passwd=self.password_db,
            db=self.name_db)

    def getCursor(self, query, params):
        try:
            cursor = self.db.cursor()
            cursor.execute(query, params)
        except Exception as e:
            self.connectDb()
            cursor = self.db.cursor()
            cursor.execute(query, params)
        self.db.commit()
        return cursor

    def annotate(self, mention_id, sentiment, name):
        if int(sentiment) == 0:
            query = """update Annotations set count_neutral = count_neutral + 1 where mention_id=%s"""
        elif int(sentiment) == 1:
            query = """update Annotations set count_pos = count_pos + 1 where mention_id=%s"""
        elif int(sentiment) == -1:
            query = """update Annotations set count_neg = count_neg + 1 where mention_id=%s"""
        else:
            query = """update Annotations set count_idk = count_idk + 1 where mention_id=%s"""
        score = """update Score set score=score+1 where name=%s"""
        try:
            #update mentions
            cursor = self.getCursor(query, (mention_id,))
            cursor.close()
            #update score
            cursor = self.getCursor(score, (name,))
            cursor.close()
        except:
            raise ValueError('Failed to update sentiment')

    def post(self):
        try:
            parser.add_argument('payload', location='form')
            args = parser.parse_args()
            args = json.loads(args['payload'])
            #verify if called coming from Slack
            if not verify_token(args['token']):
                return {
                    'error': 'Unauthorized access, GTFO'
                }
            mention_id = args['callback_id']
            value = args['actions'][0]['value']
            name = args['user']['name']
            self.annotate(mention_id, value, name)
            text = CONGRATS[randint(0,len(CONGRATS)-1)]
            return {
                'status': 'success',
                'text': text,
                'replace_original': 'true'
            }      
        except Exception as e:
            error ='ooops something went bad 😒 '  + repr(e)
            return {
                'status': 'error',
                'text': error,
                'error': repr(e)}
