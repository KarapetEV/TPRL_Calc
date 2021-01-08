import sqlite3
from PyQt5 import QtCore, QtWidgets


def create_user_list():
    con = sqlite3.connect(".\data\\users.db")
    cur = con.cursor()

    cur.execute(f'SELECT name FROM users')
    value = cur.fetchall()
    users = []
    for i in value:
        users.append(i[0])
    users.sort()
    cur.close()
    con.close()

    return users

def login(login, password):
    user = []
    con = sqlite3.connect(".\data\\users.db")
    cur = con.cursor()

    cur.execute(f'SELECT * FROM users WHERE name="{login}";')
    value = cur.fetchall()

    cur.close()
    con.close()

    if value != [] and value[0][2] == password:
        return True
    else:
        return False

def register(user, signal):
    con = sqlite3.connect(".\data\\users.db")
    cur = con.cursor()

    cur.execute(f'SELECT * FROM users WHERE name="{user[0]}";')
    value = cur.fetchall()

    if value != []:
        signal.emit('Такой пользователь существует!')
    elif value == []:
        cur.execute(f"INSERT INTO users (name, password) VALUES ('{user[0]}', '{user[1]}')")
        signal.emit(f'Пользователь {user[0]} зарегистрирован!')
        con.commit()

    cur.close()
    con.close()

if __name__ == '__main__':
    login()