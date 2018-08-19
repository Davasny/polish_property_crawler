import pymysql


class MySQL:
    def __init__(self):
        server = "localhost"
        user = "root"
        password = ""
        server_port = 3306
        database = "otodom_crawler"

        self.operating_database = pymysql.connect(host=server, user=user, password=password, database=database,
                                             charset='utf8', port=server_port)

        self.cur = self.operating_database.cursor()

    def new_query(self, command):
        if 'SELECT' in command:
            self.cur.execute(command)
            return self.cur.fetchall()
        elif 'INSERT' in command:
            self.cur.execute(command)
            self.operating_database.commit()
            return self.cur.lastrowid
        elif 'UPDATE' in command:
            self.cur.execute(command)
            self.operating_database.commit()
            return True
        elif 'DELETE' in command:
            self.cur.execute(command)
            self.operating_database.commit()
            return True
        else:
            return False
