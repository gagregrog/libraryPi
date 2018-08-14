import csv
import isbnlib


class CsvHandler:
    def __init__(self, filename='barcodes.csv'):
        self.filename = filename
        self.isbns = set()
        self.book_data = {}
        self.new_books = {}
        self.get_cache_from_csv()

    def get_cache_from_csv(self):
        try:
            with open(self.filename) as csv_file:
                lines = csv.reader(csv_file)
                for line in lines:
                    print(line)
                    isbn = line[0]
                    self.isbns.add(isbn)
                    record = {'isbn': isbn}

                    if len(line) > 1:
                        title = line[1]
                        authors = line[2:]
                        record['title'] = title
                        record['authors'] = authors

                    self.book_data[isbn] = record
        except Exception as e:
            print('[INFO] Creating File - {}'.format(self.filename))

    def add_book(self, isbn):
        if isbn not in self.isbns:
            self.isbns.add(isbn)
            try:
                book = isbnlib.meta(isbn)
                book = {
                    'isbn': isbn,
                    'title': book['Title'],
                    'authors': book['Authors']
                }
            except Exception as e:
                book = {'isbn': isbn}

            self.book_data[isbn] = book
            self.new_books[isbn] = book

            display_data = self.get_display_data(isbn)
            print("[INFO] __NEW_BOOK__ {}".format(display_data))

    def get_display_data(self, isbn):
        book = self.book_data.get(isbn)
        if book is None or book.get('title') is None:
            return isbn

        return '{} - {}'.format(book['title'], ', '.join(book['authors']))

    def write_new_to_csv(self):
        with open(self.filename, 'a+') as csv_file:
            for isbn, meta in self.new_books.items():
                row = isbn
                title = meta.get('title')

                if title is not None:
                    authors = ','.join(meta['authors'])
                    row = '{},{},{}\r\n'.format(row, title, authors)

                csv_file.write(row)
