import termios, fcntl, sys, os
from asciimatics.effects import Cycle, Stars, Julia
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import StopApplication
from asciimatics.event import KeyboardEvent
from title import title
from getpass import getpass
import bcrypt

def stop_on_keypress(event):
    if isinstance(event, KeyboardEvent):
        raise StopApplication("User terminated app")


def julia(screen):
    effects = [Julia(screen)]
    screen.play([Scene(effects)], unhandled_input=stop_on_keypress)


def concur_labs(screen):
    effects = [
        Cycle(
            screen,
            FigletText("LibraryPi", font='big'),
            int(screen.height / 2 - 8)),
        Cycle(
            screen,
            FigletText("ConcurLabs", font='small'),
            int(screen.height / 2 + 3)),
        Stars(screen, 100)
    ]
    screen.play([Scene(effects)], unhandled_input=stop_on_keypress)


def start_labs():
    Screen.wrapper(concur_labs)


def start_julia():
    Screen.wrapper(julia)


def login_or_signup():
    title("LibraryPi", "", "Concur Labs")
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    message = """
Welcome to the Concur Labs Library!

You can check out and return books at your leisure.




Please CREATE an account or LOGIN.


[1] Login to an Existing Account
    
[2] Create an Account

[J] Julia Set Visualizer

[Q] Quit

"""

    print(message)

    try:
        while 1:
            try:
                c = sys.stdin.read(1)
                if c in ['1', '2', 'j', 'J', 'q', 'Q']:
                    return c
            except IOError: pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        os.system('clear')


def signup(add_user_to_db):
    email = ''
    password = ''

    while len(email) == 0:
        title("Create an Account")
        email = input('Email: ')

    email = email.lower()

    while len(password) == 0:
        title("Create an Account")
        print("Email: {}".format(email))
        password = getpass('Password: ')

    hash = bcrypt.hashpw(password, bcrypt.gensalt(6))
    user = {'email': email, 'hash': hash}
    user = add_user_to_db(user)

    return user


def login(check_credentials_in_db):
    email = ''
    password = ''

    while len(email) == 0:
        title("Login")
        email = input('Email: ')

    email = email.lower()

    while len(password) == 0:
        title("Login")
        print("Email: {}".format(email))
        password = getpass('Password: ')

    user = {'email': email, 'password': password}
    user = check_credentials_in_db(user)

    return user


def handle_auth(add_user_to_db, check_credentials_in_db):
    while True:
        intent = login_or_signup()

        if intent == '1':
            user, error = login(check_credentials_in_db)
            if error == 'not found':
                error = 'That email address is not in our system. If this is your first time using our library, please create an account.'
            elif error == 'unauthorized':
                error = 'Your password is incorrect.'
        elif intent == '2':
            user, error = signup(add_user_to_db)
            if error == 'duplicate':
                error = 'There is already an account associated with that email address.'
        elif intent.lower() == 'j':
            start_julia()
            continue
        else:
            start_labs()
            continue

        if error:
            title("Authentication Error")

            input("""Uh oh. {}

Please press ENTER to return to the main menu.""".format(error))
            continue

        return user


def greet(user, get_display_name):
    title("Welcome, {}!".format(user[0]))

    isbns = user[2:4]
    books = [isbn for isbn in isbns if isbn != 'None']
    num_books = len(books)

    message = "You currently have {} {} checked out.".format(num_books, 'book' if num_books == 1 else 'books')

    if num_books > 0:
        message += """
[1] {}        
""".format(get_display_name(books[0]))

    if num_books > 1:
        message += """
[2] {}        
""".format(get_display_name(books[1]))

    message += "\n\nPress ENTER to continue. "
    input(message)


def display_instructions():
    title("Using the Library")
    message = """1) Wait for the video stream to initialize.

2) Hold the barcode of a book up to the camera. 
   If the camera can read it, its information will be displayed.

3) Once the book has been identified, press "O" to check it out, or "I" to check it in. 
   You may have at most two books checked out at the same time.
   
4) To quit and logout, press "Q".

Press ENTER to begin. """
    input(message)
