import sqlite3
import atexit


book_table = """CREATE TABLE IF NOT EXISTS books (
                    isbn TEXT PRIMARY KEY,
                    title TEXT,
                    author_1 TEXT,
                    author_2 TEXT,
                    author_3 TEXT,
                    publisher TEXT,
                    year TEXT,
                    created TEXT
                );"""

user_table = """CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    isbn_1 TEXT,
                    isbn_2 TEXT,
                    created TEXT
                );"""


class Database:
    def __init__(self, filename='library-pi.sqlite'):
        atexit.register(self.disconnect)
        self.conn = sqlite3.connect(filename)
        self.create_tables()
        print('[INFO] DB Loaded')
        [print(row) for row in self.get_all_books()]

    def disconnect(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        try:
            c = self.conn.cursor()
            c.execute(book_table)
            c.execute(user_table)

        except Exception as e:
            print('[ERROR] Failed to create tables')
            print(e)

    def add_user(self, user):
        try:
            c = self.conn.cursor()
            command = """INSERT OR IGNORE INTO users (id, first_name, last_name, isbn_1, isbn_2, created)
                            VALUES ("{}", "{}", "{}", "{}", "{}", CURRENT_TIMESTAMP)""".format(

                user['id'],
                user['first_name'],
                user['last_name'],
                user.get('isbn_1'),
                user.get('isbn_2'),
            )

            c.execute(command)

        except Exception as e:
            print('[ERROR] Failed to add user')
            print(e)

    def add_book(self, book):
        try:
            c = self.conn.cursor()
            command = """INSERT OR IGNORE INTO books (isbn, title, author_1, author_2, author_3, publisher, year, created)
                            VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", CURRENT_TIMESTAMP)""".format(
                book['isbn'],
                book['title'],
                book['author_1'],
                book.get('author_2'),
                book.get('author_3'),
                book['publisher'],
                book['year'])

            c.execute(command)
            print('[INFO] Adding book to database')

        except Exception as e:
            print('[ERROR] Failed to add book')
            print(e)

    def get_all_users(self):
        try:
            c = self.conn.cursor()
            command = 'SELECT * FROM users'
            c.execute(command)

            users = c.fetchall()

            return users

        except Exception as e:
            print('[ERROR] Failed to get users')
            print(e)

    def get_user(self, user_id):
        try:
            c = self.conn.cursor()
            command = 'SELECT * FROM users WHERE id="{}"'.format(user_id)
            c.execute(command)

            user = c.fetchone()

            return user

        except Exception as e:
            print('[ERROR] Failed to get users')
            print(e)

    def checkout_book(self, user_id, book_id):
        try:
            c = self.conn.cursor()
            get_user = 'SELECT isbn_1, isbn_2 FROM users WHERE id="{}"'.format(user_id)
            c.execute(get_user)

            result = c.fetchone()

            if result:
                isbn_1, isbn_2 = result
            else:
                return 'User Not Found'

            if isbn_1 == book_id or isbn_2 == book_id:
                return 'Book Already Checked Out'

            idx = 'isbn_1' if isbn_1 == 'None' else 'isbn_2' if isbn_2 == 'None' else None

            if idx:
                update_user = 'UPDATE users SET {idx}="{book_id}" WHERE id="{user_id}"'.format(
                    idx=idx, book_id=book_id, user_id=user_id)
                c.execute(update_user)

                return self.get_user(user_id)
            else:
                return 'Overdrawn'

        except Exception as e:
            print('[ERROR] Failed to check out book')
            print(e)

    def return_book(self, user_id, book_id):
        try:
            c = self.conn.cursor()
            get_user = 'SELECT isbn_1, isbn_2 FROM users WHERE id="{}"'.format(user_id)
            c.execute(get_user)

            result = c.fetchone()

            if result:
                isbn_1, isbn_2 = result
            else:
                return 'User Not Found'

            if book_id not in [isbn_1, isbn_2]:
                return 'Book Not Checked Out'

            if book_id == isbn_1:
                isbn_1 = isbn_2

            isbn_2 = 'None'

            update_user = 'UPDATE users SET isbn_1="{isbn_1}", isbn_2="{isbn_2}" WHERE id="{user_id}"'.format(
                isbn_1=isbn_1, isbn_2=isbn_2, user_id=user_id)

            c.execute(update_user)

            return self.get_user(user_id)

        except Exception as e:
            print('[ERROR] Failed to return book')
            print(e)

    def get_all_books(self):
        try:
            c = self.conn.cursor()
            command = 'SELECT * FROM books'
            c.execute(command)

            books = c.fetchall()

            return books

        except Exception as e:
            print('[ERROR] Failed to get books')
            print(e)
