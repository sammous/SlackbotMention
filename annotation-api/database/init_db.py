#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import csv

file = '***'

config = {
    'host_db': 'localhost',
    'user_db': 'root',
    'password_db': '',
    'name_db': 'Annotations'
}

if __name__ == '__main__':

    host_db = config['host_db']
    user_db = config['user_db']
    password_db = config['password_db']
    name_db = config['name_db']

    db = mdb.connect(
            host=host_db,
            user=user_db,
            passwd=password_db,
            db=name_db,
            charset='utf8')

    with open(file) as csv_dict:
        for index, line in enumerate(csv.DictReader(csv_dict)):
            text = line['description']
            alertid = line['alert_id']
            mention_id = line['id']
            url = line['url']
            cursor = db.cursor()
            query = """INSERT INTO Annotations (`mention_id`,`alert_id`,`text`,`sourceUrl`) VALUES (%s,%s,%s,%s)"""
            cursor.execute(query,(mention_id, alertid, text, url))
            db.commit()
            cursor.close()
        db.close()
