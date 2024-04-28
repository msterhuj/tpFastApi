import passlib
import sys

from app.models import User
from . import engine
from sqlmodel import Session, select
from secrets import choice
from string import digits, ascii_letters, ascii_lowercase, ascii_uppercase

keys = digits + ascii_uppercase + ascii_lowercase + ascii_letters

def random_password(size: int):
    password = ""
    for i in range(size):
        password += ''.join(choice(keys))
    return password

def main() -> None:
    print("This script create or update user password and give admin right")
    if len(sys.argv) == 1:
        print("Please provide username to create")
        return
    input("Press enter to continue")
    rand_pass = random_password(12)
    username = sys.argv[1]
    print("Press enter to set random pass")
    password = input("Set pass > ") or rand_pass
    password_confirm = input("Confirm pass > ") or rand_pass

    if password != password_confirm:
        print("Password is not eq")
        return

    if password == rand_pass:
        print("Random password set > ", rand_pass)

    with Session(engine) as session:
        user: User = session.get(User, User.name=username)



if __name__ == "__main__":
    main()
