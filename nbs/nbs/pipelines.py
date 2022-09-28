# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3


class SQLpipeline:
    def __init__(self):
        
        self.connection = sqlite3.connect('nbs.db')

        self.cursor = self.connection.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS nbs (
            [item_id] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            [title] TEXT  NOT NULL,
            [date] TEXT  NOT NULL,
            [url] TEXT  NOT NULL,
            [labels] TEXT NOT NULL,
            [links] TEXT NOT NULL,
            [body] TEXT NOT NULL

        )
        """)
    
    def process_item(self, item, spider):

        self.cursor.execute("select * from nbs where url = ?", (item['url'],))

        res = self.cursor.fetchone()

        if not res:

            self.cursor.execute("""
            INSERT INTO nbs (title, date, url, labels, links, body) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
            item['title'],
            item['date'],
            item['url'],
            str(item['labels']),
            str(item['links']),
            item['body']
            )
            )

            self.connection.commit()
        return item
