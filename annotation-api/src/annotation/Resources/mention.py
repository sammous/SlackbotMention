import MySQLdb as mdb
from random import randint
from flask import request
from flask_restful import Resource
#from form_parser import parse


class Mention(Resource):

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
        query = """SELECT mention_id, text
            FROM Annotations LIMIT 1 OFFSET %s"""%randint(1,self.count)

        cursor = self.getCursor(query)
        numrows = int(cursor.rowcount)

        if numrows == 0:
            raise ValueError("No more mention to annotate")

        result = cursor.fetchone()
        cursor.close()
        return {'mention_id':result[0],
                'text': result[1]}

    def get(self):
        try:
            res = self.extractMention()
            return {
                'status': 'success',
                'mention_id': res['mention_id'],
                'text': res['text']
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': repr(e)}

class Annotate(Resource):

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

    def annotate(self, mention_id, sentiment):
        if int(sentiment) == 0:
            field = 'count_neutral'
        elif int(sentiment) == 1:
            field = 'count_pos'
        elif int(sentiment) == -1:
            field = 'count_neg'
        else:
            field = 'count_idk'
        query = """UPDATE Annotations SET %s=%s + 1 WHERE mention_id=%s""" %(field,field,mention_id)
        try:
            cursor = self.getCursor(query)
            cursor.close()
        except:
            raise ValueError('Failed to update sentiment')

    #@parse('annotate_post')
    def post(self, args):
        try:
            self.annotate(args['mention_id'], args['sentiment'])
            return {
                'status': 'success'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': repr(e)}

class Information(Resource):

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

    def computeInformation(self):
        query1= """SELECT * FROM Annotations WHERE (count_pos, count_neg, count_neutral, count_idk) != (0,0,0,0)"""
        cursor1 = self.getCursor(query1)
        total_annotated = int(cursor1.rowcount)

        query2 = """SELECT * FROM Annotations WHERE count_pos != 0"""
        cursor2 = self.getCursor(query2)
        total_positive = int(cursor2.rowcount)

        query3 = """SELECT * FROM Annotations WHERE count_neutral != 0"""
        cursor3 = self.getCursor(query3)
        total_neutral = int(cursor3.rowcount)

        query4 = """SELECT * FROM Annotations WHERE count_neg != 0 """
        cursor4 = self.getCursor(query4)
        total_negative = int(cursor4.rowcount)

        query5 = """SELECT * FROM Annotations WHERE count_idk != 0 """
        cursor5 = self.getCursor(query5)
        total_idk = int(cursor5.rowcount)

        query6 = """SELECT * FROM Annotations"""
        cursor6 = self.getCursor(query6)
        total_mentions = int(cursor6.rowcount)

        mentions_left = total_mentions - total_annotated

        cursor1.close()
        cursor2.close()
        cursor3.close()
        cursor4.close()
        cursor5.close()
        cursor6.close()

        return {
            "totalMentions": total_mentions,
            "totalAnnotated": total_annotated,
            "annotationLeft": mentions_left,
            "positive": total_positive,
            "negative": total_negative,
            "neutral": total_neutral,
            "idk": total_idk
        }

    def get(self):
        try:
            res = self.computeInformation()
            return {
                'status': 'success',
                "totalMentions": res['totalMentions'],
                "totalAnnotated": res['totalAnnotated'],
                "annotationLeft": res['annotationLeft'],
                "positive": res['positive'],
                "negative": res['negative'],
                "neutral": res['neutral'],
                "idk": res['idk']
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': repr(e)}

class Leaderboard(Resource):

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

    def get_leaderboard(self):
        query = """SELECT * FROM Score ORDER BY score DESC;"""
        cursor = self.getCursor(query)
        return list(cursor)

    def post(self):
        try:
            users = self.get_leaderboard()
            attachments = []
            for i, t in enumerate(users):
                if i == 0:
                    text = "%s. 🏅%s score: %s"%(1, t[1], t[2])
                elif i == 1:
                    text = "%s. 🎖%s score: %s"%(2, t[1], t[2])
                elif i == 2:
                    text = "%s. 🎗%s score: %s"%(3, t[1], t[2])
                elif i == len(users) - 1:
                    text = "%s. :troll: %s score: %s"%(i+1, t[1], t[2])
                else:
                    text = "%s. %s score: %s"%(i+1, t[1], t[2])
                attachments.append(
                    {
                        "text": text
                    }
                )
            return {
                "text": "🏆 Leaderboard for Sentiment Annotations 🏆",
                "attachments": attachments
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': repr(e)}
