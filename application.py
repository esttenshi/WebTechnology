from flask import Flask
from flask_restful import Api
import sqlite3

app = Flask(__name__, template_folder='Templates')
api = Api(app)

#для кириллицы
app.json.ensure_ascii = False

#подключение к БД
con = sqlite3.connect('database.db', check_same_thread=False)





