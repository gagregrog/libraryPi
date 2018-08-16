from database import Database
import command_line
db = Database()

command_line.start_labs()
while True:
    user = command_line.handle_auth(db.add_user, db.check_credentials)
    
