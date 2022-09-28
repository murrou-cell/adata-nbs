import sqlite3
from mk_resp import response_mk

class litewrapper(response_mk):
    def __init__(self):
        try:
            self.conn = sqlite3.connect('nbs\\nbs.db')
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)

    def query_by_id(self, table, column, _id):

        self.cursor.execute(f"SELECT * FROM {table} WHERE {column} = {_id}")

        resp = self.cursor.fetchall()

        response = self.build_repsonse_many(resp)

        return response
    
    def query_all(self, table):
       
        self.cursor.execute(f"SELECT * FROM {table}")
        all_ = self.cursor.fetchall()

        response = self.build_repsonse_many(all_)

        return response

    def query_many(self, table, column, sstring):
    
        self.cursor.execute(f"SELECT * FROM {table} WHERE {column} LIKE '%{sstring}%'")

        resp = self.cursor.fetchall()

        response = self.build_repsonse_many(resp)

        return response


    def update_one(self, item_id ,data, table='nbs', column='item_id'):
        

        exists = True if len(self.query_by_id(table, column, item_id)) > 0 else False
        if exists:
            self.cursor.execute(f"UPDATE nbs SET title = ?, date = ?, url = ?, labels = ?, links = ?, body = ? WHERE item_id = ?", (data.title, data.date, data.url, str(data.labels), str(data.links), data.body, item_id))

            resp = self.conn.commit()

            return {'message': f"{item_id} - UPDATED"}
        return {'message': "NON EXISTING ITEM"}

    def delete_one(self, table, column, sstring):
        
        self.cursor.execute(f"DELETE from {table} WHERE {column} = {sstring}")
        
        self.conn.commit()

        return {"message": f"{sstring} - DELETED"}

