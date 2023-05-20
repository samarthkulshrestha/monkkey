import pickle
from getpass import getpass

from colors import colors
from encdec import (
    decrypt_AES_GCM,
    encrypt_AES_GCM,
)
from menu import (
    create_pass,
    menu,
    read_pass,
)
from set_new_master_pass import (
    set_new_master_password,
)

try:
    mp = pickle.load(
        open("master.txt", "rb")
    )
    mpp = getpass(
        "enter master password: "
    ).encode("utf-8")

    try:
        masterPass = decrypt_AES_GCM(
            mp, mpp
        )
    except:
        print(
            f"{colors.FAIL}master password is incorrect{colors.ENDC}"
        )
        quit()

    print(
        f"""{colors.OKBLUE}welcome! type 'h' or 'help' and press enter for a help message{colors.ENDC}"""
    )
    menu(mpp)
except IOError:
    mpp = getpass(
        "set new master password: "
    ).encode("utf-8")
    set_new_master_password(mpp)
