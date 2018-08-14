from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import cv2
import isbn

outfile = "barcodes.csv"
red = (0, 0, 255)

print("[INFO] Starting stream...")

vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

found_barcodes = set()

csv = open(outfile, "w")

while True:
    frame = vs.read()

    height, width = frame.shape[:2]
    new_height = 400 / width * height

    frame = cv2.resize(frame, (400, int(new_height)), interpolation=cv2.INTER_CUBIC)
    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), red, 2)

        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        
        cv2.putText(frame, str(barcode_data), (x, y - 20),
            cv2.FONT_HERSHEY_SIMPLEX,0.5, red, 2)
       
        if barcode_data not in found_barcodes:
            csv.write("{}\r\n".format(barcode_data))
            csv.flush()
            found_barcodes.add(barcode_data)
            title = isbn.get_title_from_isbn(barcode_data)
            
            print("[INFO] {}: {}".format(barcode_type, barcode_data))
            print("[INFO] Title:  {}".format(title)) 

    cv2.imshow("Barcode Scanner", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

print("[INFO] Closing stream...")
csv.close()
cv2.destroyAllWindows()
vs.stop()
