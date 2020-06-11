import pymysql

class DataLoader:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        self.con = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        self.cur = self.con.cursor()

    def close_conn(self):
        self.cur.close()
        self.con.close()

    def get_data(self, q):
        self.connect()
        self.cur.execute(q)
        self.data = self.cur.fetchall()
