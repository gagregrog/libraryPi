from imutils.video import VideoStream
from pyzbar import pyzbar
import platform
import time
import cv2
from handle_csv import CsvHandler
import isbnlib
from database import Database

red = (0, 0, 255)
csv = CsvHandler()
db = Database()

print("[INFO] Starting stream...")
camera = {"usePiCamera": True} if platform.system() == 'Linux' else {"src": 0}
vs = VideoStream(**camera).start()
time.sleep(1.0)

while True:
    frame = vs.read()
    height, width = frame.shape[:2]
    new_height = 800 / width * height
    frame = cv2.resize(frame, (800, int(new_height)), interpolation=cv2.INTER_CUBIC)

    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        isbn = barcode.data.decode("utf-8")

        if isbnlib.notisbn(isbn):
            continue

        barcode_type = barcode.type
        qr_code = barcode_type == 'QRCODE'

        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), red, 2)

        display_name = csv.add_book(isbn, qr_code, db.add_book)

        if display_name:
            cv2.putText(frame, display_name, (x, y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, red, 2)

    cv2.imshow("Barcode Scanner", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

print("[INFO] Closing stream...")
csv.write_new_to_csv()
cv2.destroyAllWindows()
vs.stop()
