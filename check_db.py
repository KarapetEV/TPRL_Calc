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

    decrypt_pass = decrypt(value[0][2])

    if value != [] and decrypt_pass == password:
        return True
    else:
        return False

def register(user, signal):
    con = sqlite3.connect(".\data\\users.db")
    cur = con.cursor()

    cur.execute(f'SELECT * FROM users WHERE name="{user[0]}";')
    value = cur.fetchall()

    encrypt_pass = encrypt(user[1])

    if value != []:
        signal.emit('Такой пользователь существует!')
    elif value == []:
        cur.execute(f"INSERT INTO users (name, password) VALUES ('{user[0]}', '{encrypt_pass}')")
        signal.emit(f'Пользователь {user[0]} зарегистрирован!')
        con.commit()

    cur.close()
    con.close()

def encrypt(line):
    result = ""
    for i in range(len(line)):
        char = line[i]
        result += chr(ord(char) * 2 - 10)
    return result

def decrypt(line):
    result = ""
    for i in range(len(line)):
        char = line[i]
        result += chr(int((ord(char) + 10) / 2))
    return result


if __name__ == '__main__':
    login()