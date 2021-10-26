from getpass import getpass
from encdec import encrypt_AES_GCM, decrypt_AES_GCM
from menu import menu, create_pass, read_pass
from master import mp
from set_new_master_pass import set_new_master_password

if mp == None:
    mpp = getpass("enter new master password: ").encode("utf-8")
    set_new_master_password(mpp)
else:
    mpp = getpass("enter master password: ").encode("utf-8")

    try:
        masterPass = decrypt_AES_GCM(mp, mpp)
    except:
        print("fuck off!")
        quit()

    print("welcome!")
    menu(mpp)
