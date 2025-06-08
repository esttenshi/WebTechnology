import sqlite3

con = sqlite3.connect('../database/database.db')

class Accounts:
    def createTable(self):
        with con:
            data = con.execute("""select
                                     count(*)
                                   from
                                     sqlite_master
                                   where
                                     type='table'
                                     and name='accounts'""")
            for row in data:
                if row[0] == 0:
                    with con:
                        con.execute("""
                             CREATE TABLE accounts (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                login TEXT,
                                password TEXT
                             );
                         """)

    def insertTestData(self):
        sql = """INSERT INTO accounts 
                (login, password) 
                values(?, ?)"""

        data = [  # тестовые данные
            ('admin', 'admin'),
            ('esttenshi', 'esttenshi'),
            ('jilietka', 'jilietka')

        ]

        with con:
            con.executemany(sql, data)

        with con:
            data = con.execute("SELECT * FROM accounts")
            for row in data:
                print(row)

    def connect(self):
        self.createTable()
        self.insertTestData()


class Clubs:
    def createTable(self):
        with con:
            data = con.execute("""select
                                     count(*)
                                   from
                                     sqlite_master
                                   where
                                     type='table'
                                     and name='clubs'""")
            for row in data:
                if row[0] == 0:
                    with con:
                        con.execute("""
                             CREATE TABLE clubs (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                head INTEGER,
                                connection INTEGER
                             );
                         """)

    def insertTestData(self):
        sql = """INSERT INTO clubs 
                (title, head, connection) 
                values(?, ?, ?)"""

        data = [  # тестовые данные
            ('КВН', '2', '1')
        ]

        with con:
            con.executemany(sql, data)

        with con:
            data = con.execute("SELECT * FROM clubs")
            for row in data:
                print(row)

    def connect(self):
        self.createTable()
        self.insertTestData()


class Connection:
    def createTable(self):
        with con:
            data = con.execute("""select
                                     count(*)
                                   from
                                     sqlite_master
                                   where
                                     type='table'
                                     and name='connection'""")
            for row in data:
                if row[0] == 0:
                    with con:
                        con.execute("""
                             CREATE TABLE connection (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                telegram TEXT
                             );
                         """)

    def insertTestData(self):
        sql = """INSERT INTO connection 
                (telegram) 
                values(?)"""

        data = [  # тестовые данные
            ('@esttenshi',)
        ]

        with con:
            con.executemany(sql, data)

        with con:
            data = con.execute("SELECT * FROM connection")
            for row in data:
                print(row)

    def connect(self):
        self.createTable()
        self.insertTestData()


class Status:
    def createTable(self):
        with con:
            data = con.execute("""select
                                     count(*)
                                   from
                                     sqlite_master
                                   where
                                     type='table'
                                     and name='status'""")
            for row in data:
                if row[0] == 0:
                    with con:
                        con.execute("""
                             CREATE TABLE status (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT
                             );
                         """)

    def insertTestData(self):
        sql = """INSERT INTO status 
                (title) 
                values(?)"""

        data = [  # тестовые данные
            ('Администратор',),
            ('Руководитель',),
            ('Студент',)

        ]

        with con:
            con.executemany(sql, data)

        with con:
            data = con.execute("SELECT * FROM status")
            for row in data:
                print(row)

    def connect(self):
        self.createTable()
        self.insertTestData()


class Users:
    def createTable(self):
        with con:
            data = con.execute("""select
                                     count(*)
                                   from
                                     sqlite_master
                                   where
                                     type='table'
                                     and name='users'""")
            for row in data:
                if row[0] == 0:
                    with con:
                        con.execute("""
                             CREATE TABLE users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                surname TEXT,
                                name TEXT,
                                patronymic TEXT,
                                status INTEGER,
                                clubs INTEGER
                             );
                         """)

    def insertTestData(self):
        sql = """INSERT INTO users 
                (surname, name, patronymic, status, clubs) 
                values(?, ?, ?, ?, ?)"""

        data = [  # тестовые данные
            ('Герасимов', 'Владислав', 'Владимирович', '1', None),
            ('Тарабановская', 'Екатерина', 'Сергеевна', '2', '1'),
            ('Калинина', 'Юлия', 'Юрьевна', '3', '1')
        ]

        with con:
            con.executemany(sql, data)

        with con:
            data = con.execute("SELECT * FROM users")
            for row in data:
                print(row)

    def connect(self):
        self.createTable()
        self.insertTestData()

Accounts().connect()
Clubs().connect()
Connection().connect()
Status().connect()
Users().connect()
