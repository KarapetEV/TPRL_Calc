import sqlite3
from PyQt5 import QtCore, QtWidgets


def create_user_list():
    con = sqlite3.connect("data/data.db")
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
    con = sqlite3.connect("data/data.db")
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
    con = sqlite3.connect("data/data.db")
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


def save_project(user, info):
    con = sqlite3.connect("data/data.db")
    cur = con.cursor()

    cur.execute(f"SELECT user_id FROM users WHERE name='{user}'")
    value = cur.fetchone()

    entry_data = value + info

    cur.execute('INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', entry_data)
    con.commit()

    cur.close()
    con.close()


def load_project(name, state):
    con = sqlite3.connect("data/data.db")
    cur = con.cursor()

    cur.execute(f"SELECT user_id FROM users WHERE name='{name}'")
    user_id = cur.fetchone()[0]

    cur.execute(f'''SELECT project_num, 
                          date, 
                          theme, 
                          initiator, 
                          customer, 
                          save_date
                    FROM projects 
                    WHERE user_id="{user_id}" AND state="{state}"''')
    value = cur.fetchall()

    cur.close()
    con.close()

    return value


def get_project(data):
    con = sqlite3.connect("data/data.db")
    cur = con.cursor()

    user_id = cur.execute(f"SELECT user_id FROM users WHERE name='{data[0]}'").fetchone()[0]

    cur.execute(f"SELECT state, path, params FROM projects WHERE user_id='{user_id}' AND project_num='{data[1]}' AND save_date='{data[2]}'")
    value = cur.fetchone()

    cur.close()
    con.close()

    return value


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
