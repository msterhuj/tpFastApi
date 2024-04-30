"""
This script create or update user password and give admin right
this is not a part of the app, this is a helper script to initialize the app
"""

from sys import argv
from secrets import choice
from string import digits, ascii_letters, ascii_lowercase, ascii_uppercase

from sqlmodel import Session, select

from . import engine
from .database import create_db_and_tables
from app.models import User, get_hashed_password

keys = digits + ascii_uppercase + ascii_lowercase + ascii_letters


def random_password(size: int):
    password = ""
    for i in range(size):
        password += ''.join(choice(keys))
    return password


def main() -> None:
    print("This script create or update user password and give admin right")
    if len(argv) == 1:
        print("Please provide username to create")
        return
    input("Press enter to continue")
    rand_pass = random_password(12)
    username = argv[1]
    print("Press enter to set random pass")
    password = input("Set pass > ") or rand_pass
    password_confirm = input("Confirm pass > ") or rand_pass

    if password != password_confirm:
        print("Password is not eq")
        return

    with Session(engine) as session:
        user: User = session.exec(select(User).filter(User.name == username)).first()
        if not user:
            print("User not found creating new user")
            user = User(name=username)

        user.password = get_hashed_password(password)
        user.is_admin = True
        session.add(user)
        session.commit()
        print("User created or updated")
        print("Username: ", user.name)
        if password == rand_pass:
            print("Random password set > ", rand_pass)
        print("Admin rights given")


if __name__ == "__main__":
    create_db_and_tables(engine)
    main()
