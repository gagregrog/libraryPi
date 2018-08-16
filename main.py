from os import system
from database import Database
from handle_csv import CsvHandler
from barcode_scanner import start_scanner
import command_line
import atexit


def start_app():
    db = Database()
    csv = CsvHandler()
    atexit.register(csv.write_new_to_csv)
    atexit.register(db.disconnect)

    # command_line.start_labs()
    while True:
        user, new_user = command_line.handle_auth(db.add_user, db.check_credentials)
        if new_user:
            command_line.display_instructions(True)
        else:
            command_line.greet(user, csv.get_display_data)
        start_scanner(db, csv, user)


if __name__ == '__main__':
    try:
        start_app()
    except KeyboardInterrupt:
        system('clear')
