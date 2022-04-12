"""Handles User and its commands"""
import os
from pathlib import Path
from sqlite3 import connect as connect_sqlite3


def exec_sql(sql: str, values=()):
    """Execites SQL queries and returns output as a list"""
    conn = connect_sqlite3(str(Path(__file__).parent / 'sqlite3.db'))
    cur = conn.cursor()
    output = list(cur.execute(sql, values))
    conn.commit()
    conn.close()

    return output

# Creating Table if not existing
exec_sql('CREATE TABLE IF NOT EXISTS users (username TEXT UNIQUE, password TEXT)')


class User:
    """Handles User and its commands"""
    def __init__(self, username, password):
        """Initialiser"""
        self.username = username
        self.password = password
        self.user_folder = Path(__file__).parent / 'users' / username
        self.curr_dir = self.user_folder
        self.valid = False

    def register(self):
        """Reistration Handler"""
        if self.user_folder.exists():
            return 'Username Exists'

        exec_sql('INSERT INTO users VALUES (?, ?)',
                 (self.username, self.password))
        self.user_folder.mkdir()
        return self.login()

    def login(self):
        """Login Handler"""
        output = exec_sql(
            'SELECT username FROM users WHERE username=? AND password=?', (self.username, self.password))

        if len(output) == 0:
            return 'Couldn\'t find one with such credentials'

        self.valid = True
        return f'Logged in as {self.username}'

    def cd(self, to):
        """Changes Directory"""
        if not self.valid:
            return 'Login / Register first'
        to = (self.curr_dir / to).resolve()

        if to.exists() and to.is_dir() and self.username in to.parts:
            self.curr_dir = to
            return 'Done'
        return "Not A Directory"

    def ls(self):
        """Lists Content in Current Directory"""
        if not self.valid:
            return 'Login / Register first'
        return str(os.listdir(self.curr_dir))

    def mkdir(self, name):
        """Makes a directory in current Directory"""
        if not self.valid:
            return 'Login / Register first'
        folder = (self.curr_dir / name).resolve()

        if folder.exists():
            return 'Already Exists'

        if self.username in folder.parts:
            folder.mkdir()
            return 'Done'

        return 'Not Accessible'

    def cat(self, name):
        """Shows Content in a file"""
        if not self.valid:
            return 'Login / Register first'
        file = (self.curr_dir / name).resolve()

        if file.exists() and file.is_file() and self.username in file.parts:
            return file.read_text()
        return "Not A Directory"

    def file_append(self, name, content):
        """Appends Content in a given file (Even Creates if not present)"""
        if not self.valid:
            return 'Login / Register first'
        file = (self.curr_dir / name).resolve()
        with open(file, 'a', encoding='utf-8') as f:
            f.write(content)
        return 'Done'
