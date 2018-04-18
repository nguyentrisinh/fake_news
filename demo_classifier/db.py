import psycopg2

class Connection():
    hostname = 'localhost'
    username = 'postgres'  # the username when you create the database
    password = '123456'  # change to your password
    database = 'fake_news_db'
    conn = None
    def connect(self):
        self.conn = psycopg2.connect(host=self.hostname, user=self.username, password=self.password,
                                     dbname=self.database)
    def query(self,query):
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()
    def close(self):
        self.conn.close()