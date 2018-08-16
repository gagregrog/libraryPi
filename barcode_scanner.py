from imutils.video import VideoStream
from pyzbar import pyzbar
from os import system
import platform
import time
import cv2
import isbnlib

red = (0, 0, 255)
black = (0, 0, 0)
video_width = 800


def exists(isbn):
    return isbn if isbn != 'None' else None


def get_user_books(user):
    return [exists(book) for book in user[2:4]]


def can_checkout(isbn, user):
    isbns = get_user_books(user)

    if isbn in isbns:
        return False, 'You have already checked out this book.'
    elif isbns[1]:
        return False, 'You already have two books checked out.\n\nPlease return one before checking out another.'
    else:
        return True, None


def start_scanner(db, csv, user):
    system('clear')
    print("[INFO] Starting stream...\n")
    camera = {"usePiCamera": True} if platform.system() == 'Linux' else {"src": 0}
    vs = VideoStream(**camera).start()
    time.sleep(1.0)
    last_book_found = {}

    while True:
        isbn_1, isbn_2 = get_user_books(user)
        if isbn_2:
            books_remaining = 0
        elif isbn_1:
            books_remaining = 1
        else:
            books_remaining = 2

        frame = vs.read()
        height, width = frame.shape[:2]
        new_height = int(video_width / width * height)
        frame = cv2.resize(frame, (video_width, new_height), interpolation=cv2.INTER_CUBIC)

        barcodes = pyzbar.decode(frame)

        for barcode in barcodes:
            isbn = barcode.data.decode("utf-8")

            if isbnlib.notisbn(isbn):
                continue

            qr_code = barcode.type == 'QRCODE'

            (x, y, w, h) = barcode.rect
            if int(w) < 100 or int(h) < 40:
                continue

            cv2.rectangle(frame, (x, y), (x + w, y + h), red, 2)

            found_book = csv.add_book(isbn, qr_code, db.add_book)

            if found_book:
                cv2.putText(frame, found_book['display_name'], (x, y - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, red, 1.5)
                if found_book['isbn'] != last_book_found.get('isbn'):
                    last_book_found = found_book

                    print("""Title: {}
Authors: {}
Year: {}
Publisher: {}

""".format(found_book['title'], found_book['authors'], found_book['year'], found_book['publisher']))

        # Display user's email on video
        cv2.putText(frame, user[0], (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, black, 2)

        # Display checked out quantity on video
        cv2.putText(frame, 'Books Remaining: {}'.format(books_remaining), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, black, 2)

        title = last_book_found.get('title')
        if title:
            cv2.putText(frame, "Selected: {}".format(title), (10, new_height - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, red, 2)

        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF

        if key in [ord("q"), ord("Q")]:
            break

        if last_book_found.get('title'):
            if key in [ord("O"), ord("o")]:
                isbn = last_book_found['isbn']
                ok, error = can_checkout(isbn, user)
                if ok:
                    updated_user, error = db.checkout_book(user[0], isbn)

                    if updated_user:
                        user = updated_user
                        print("Successfully checked out {}!\n".format(last_book_found['title']))
                    else:

                        print('[ERROR] Something went wrong', error)
                else:
                    print('[ERROR] ', error)

                last_book_found = {}


            if key in [ord("I"), ord("i")]:
                print('want to checkin')

    print("[INFO] Closing stream...")
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    vs.stop()
