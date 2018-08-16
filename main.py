from database import Database
from handle_csv import CsvHandler
import command_line

db = Database()
csv = CsvHandler()

# command_line.start_labs()
while True:
    user = command_line.handle_auth(db.add_user, db.check_credentials)
    command_line.greet(user, csv.get_display_data)
    command_line.display_instructions()
