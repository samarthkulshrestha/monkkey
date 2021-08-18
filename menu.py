from getpass import getpass
from passwordgenerator import pwgenerator
from encdec import encrypt_AES_GCM, decrypt_AES_GCM
import sqlite3
from datetime import datetime
import pyperclip


con = sqlite3.connect('pws.db', detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()


def menu(mpp):
    print("-" * 30)
    print(("-" * 13) + "Menu" + ("-" * 13))
    print("1. create new password")
    print("2. find a password")
    print("3. update passwords")
    print("Q. exit")
    print("-" * 30)
    choice = input("[1/2/3/Q]: ")

    if choice == "1":
        create_pass(mpp)

    if choice == "2":
        read_pass(mpp)

    if choice == "3":
        update_pass(mpp)

    # if choice == "m":
    #     update_master_pass(mpp)

    else:
        quit()


def create_pass(mpp):
    service_name = input("enter the name of the service: ")
    service_url = input("enter the URL of the service: ")
    identifier = input("enter the identifier [username/email]: ")
    ent_or_gen = input("do you want to auto-generate a strong password? [y/n]: ")

    if ent_or_gen == "y":
        password = pwgenerator.generate()
        pyperclip.copy(password)
        print("password copied to clipboard!")
    else:
        password = getpass("enter the password: ")
        c_password = getpass("confirm the password: ")

        if password == c_password:
            pass
        else:
            print("passwords do not match!")
            password = getpass("enter the password: ")
            c_password = getpass("confirm the password: ")

            if password == c_password:
                pass
            else:
                print("two failed attempts!")
                quit()


    enc_password = encrypt_AES_GCM(password.encode("utf-8"), mpp)

    kdf_salt = enc_password[0]
    ciphertext = enc_password[1]
    nonce = enc_password[2]
    auth_tag = enc_password[3]

    cur.execute("INSERT INTO passwords VALUES (?,?,?,?,?,?,?,?)", (service_name, service_url, identifier, kdf_salt, ciphertext, nonce, auth_tag, datetime.now()))

    con.commit()

    menu(mpp)


def read_pass(mpp):
    service_name = input("enter the name of the service: ")

    cur.execute("SELECT kdf_salt, ciphertext, nonce, auth_tag FROM passwords WHERE service_name=(?)", (service_name,))
    pw = cur.fetchone()

    dec_pass = decrypt_AES_GCM(pw, mpp)
    dec_pass = dec_pass.decode("utf-8")

    pyperclip.copy(dec_pass)
    print("password copied to clipboard!")

    menu(mpp)

def update_pass(mpp):
    service_name = input("enter the name of the service: ")
    print(f"updating the password for {service_name} account")

    ent_or_gen = input("do you want to auto-generate a strong password? [y/n/q]: ")

    if ent_or_gen == "y":
        password = pwgenerator.generate()
        pyperclip.copy(password)
        print("password copied to clipboard!")
    elif ent_or_gen == "n":
        password = getpass("enter the password: ")
        c_password = getpass("confirm the password: ")

        if password == c_password:
            pass
        else:
            print("passwords do not match!")
            password = getpass("enter the password: ")
            c_password = getpass("confirm the password: ")

            if password == c_password:
                pass
            else:
                print("two failed attempts!")
                quit()
    else:
        quit()

    enc_password = encrypt_AES_GCM(password.encode("utf-8"), mpp)

    kdf_salt = enc_password[0]
    ciphertext = enc_password[1]
    nonce = enc_password[2]
    auth_tag = enc_password[3]

    cur.execute("UPDATE passwords SET kdf_salt=? ,ciphertext=?, nonce=?, auth_tag=?, created_at=? WHERE service_name=? ", (kdf_salt, ciphertext, nonce, auth_tag, datetime.now(), service_name))

    con.commit()
    menu(mpp)
