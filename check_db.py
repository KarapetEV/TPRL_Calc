# -*- coding: utf-8 -*-

# © Copyright 2021 Aleksey Karapyshev, Evgeniy Karapyshev
# E-mail: <karapyshev@gmail.com>, <karapet2011@gmail.com>

# This file is part of TPRL Calculator.
#
#     TPRL Calculator is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Foobar is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Foobar.  If not, see <https://www.gnu.org/licenses/>.

import sqlite3


def create_db():
    con = sqlite3.connect("data/data.db")
    cur = con.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS "projects" ('
                '"user_id"	INTEGER,'
                '"project_num"	TEXT,'
                '"date"	TEXT,'
                '"theme"	TEXT,'
                '"initiator"	TEXT,'
                '"customer"	TEXT,'
                '"save_date"	TEXT,'
                '"state"	TEXT,'
                '"path"	TEXT,'
                '"params"	TEXT,'
                'FOREIGN KEY("user_id") REFERENCES "users"("user_id")'
                ')')

    cur.execute('CREATE TABLE IF NOT EXISTS "users" ('
                '"user_id"	INTEGER,'
                '"name"	TEXT NOT NULL UNIQUE,'
                '"password"	TEXT NOT NULL,'
                'PRIMARY KEY("user_id" AUTOINCREMENT)'
                ')')
    con.commit()
    cur.close()
    con.close()


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

    cur.execute(f"SELECT state, path, params, project_num, date, theme, initiator, customer FROM projects WHERE user_id='{user_id}' AND project_num='{data[1]}' AND save_date='{data[2]}'")
    value = cur.fetchone()

    cur.close()
    con.close()

    return value

def remove_project(data):
    con = sqlite3.connect("data/data.db")
    cur = con.cursor()

    user_id = cur.execute(f"SELECT user_id FROM users WHERE name='{data[0]}'").fetchone()[0]

    cur.execute(f"SELECT path "
                f"FROM projects "
                f"WHERE user_id='{user_id}' AND project_num='{data[1]}' AND save_date='{data[2]}'")
    value = cur.fetchone()[0]

    cur.execute(f"DELETE FROM projects WHERE user_id='{user_id}' AND project_num='{data[1]}' AND save_date='{data[2]}'")
    con.commit()

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
