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


def start_scanner(db, csv, user):
    system('clear')
    print("[INFO] Starting stream...\n")
    camera = {"usePiCamera": True} if platform.system() == 'Linux' else {"src": 0}
    vs = VideoStream(**camera).start()
    time.sleep(1.0)
    last_book_found = {}

    while True:
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
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, red, 2)
                if found_book['isbn'] != last_book_found.get('isbn'):
                    last_book_found = found_book

                    print("""Title: {}
Authors: {}
Year: {}
Publisher: {}

""".format(found_book['title'], found_book['authors'], found_book['year'], found_book['publisher']))

        cv2.putText(frame, user[0], (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, black, 2)
        title = last_book_found.get('title')
        if title:
            cv2.putText(frame, "Selected: {}".format(title), (10, new_height - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)

        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    print("[INFO] Closing stream...")
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    vs.stop()
