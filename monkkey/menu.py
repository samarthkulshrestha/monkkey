from datetime import datetime
from getpass import getpass

import pyperclip
import sqlite3 as sql
from passwordgenerator import pwgenerator

from colors import colors
from encdec import (
    decrypt_AES_GCM,
    encrypt_AES_GCM,
)

con = sql.connect("pws.db")
cur = con.cursor()


def menu(mpp):
    choice = input(
        f"\n{colors.OKBLUE}>{colors.ENDC} "
    ).lower()

    if choice == "in" or choice == "init":
        init_db(mpp)

    if choice == "a" or choice == "add":
        create_pass(mpp)

    if choice == "r" or choice == "read":
        read_pass(mpp)

    if choice == "u" or choice == "update":
        update_pass(mpp)

    if choice == "i" or choice == "info":
        get_info(mpp)

    if choice == "m" or choice == "master":
        update_master_pass()

    if choice == "h" or choice == "help":
        show_help(mpp)

    else:
        quit()


def init_db(mpp):
    try:
        cur.execute(
            """CREATE TABLE passwords (service_name text UNIQUE, service_url text
                                       UNIQUE, identifier text, kdf_salt blob,
                                       ciphertext blob, nonce blob, auth_tag blob,
                                       created_at date);"""
        )
        print(
            f"{colors.OKGREEN}database initialized{colors.ENDC}"
        )
    except sql.OperationalError:
        print(
            f"""{colors.WARNING}database has been initialized already.{colors.ENDC}"""
        )

    menu(mpp)


def create_pass(mpp):
    service_name = input(
        "enter the name of the service: "
    ).lower()
    service_url = input(
        "enter the URL of the service: "
    ).lower()
    identifier = input(
        "enter the identifier [username/email]: "
    )
    ent_or_gen = input(
        "do you want to auto-generate a strong password? [y/n]: "
    ).lower()

    if ent_or_gen == "y":
        password = pwgenerator.generate()
        pyperclip.copy(password)
        print(
            f"{colors.OKGREEN}password copied to clipboard{colors.ENDC}"
        )
    else:
        password = getpass(
            "enter the password: "
        )
        c_password = getpass(
            "confirm the password: "
        )

        if password == c_password:
            pass
        else:
            print(
                f"{colors.WARNING}passwords do not match{colors.ENDC}"
            )
            password = getpass(
                "enter the password: "
            )
            c_password = getpass(
                "confirm the password: "
            )

            if password == c_password:
                pass
            else:
                print(
                    f"{colors.FAIL}two failed attempts{colors.ENDC}"
                )
                quit()

    enc_password = encrypt_AES_GCM(
        password.encode("utf-8"), mpp
    )

    kdf_salt = enc_password[0]
    ciphertext = enc_password[1]
    nonce = enc_password[2]
    auth_tag = enc_password[3]

    try:
        cur.execute(
            "INSERT INTO passwords VALUES (?,?,?,?,?,?,?,?)",
            (
                service_name,
                service_url,
                identifier,
                kdf_salt,
                ciphertext,
                nonce,
                auth_tag,
                datetime.now(),
            ),
        )

        con.commit()

    except sql.IntegrityError:
        print(
            f"""{colors.WARNING}a record for the entered service already exists,
            use the help command for help{colors.ENDC}"""
        )

    menu(mpp)


def read_pass(mpp):
    service_name = input(
        "enter the name of the service: "
    )

    try:
        cur.execute(
            """SELECT kdf_salt, ciphertext, nonce, auth_tag FROM passwords WHERE
            service_name=(?)""",
            (service_name,),
        )
    except sql.OperationalError:
        print(
            f"""{colors.WARNING}database is not initialized yet,
            use the init command to do so{colors.ENDC}"""
        )

    pw = cur.fetchone()

    if pw is not None:
        dec_pass = decrypt_AES_GCM(pw, mpp)
        dec_pass = dec_pass.decode("utf-8")

        pyperclip.copy(dec_pass)
        print(
            f"{colors.OKGREEN}password copied to clipboard{colors.ENDC}"
        )
    else:
        print(
            f"{colors.WARNING}password for the entered service does not exist{colors.ENDC}"
        )

    menu(mpp)


def update_pass(mpp):
    service_name = input(
        "enter the name of the service: "
    )
    print(
        f"{colors.OKBLUE}updating the password for your{colors.ENDC} {colors.OKGREEN}{service_name} account{colors.ENDC}"
    )

    ent_or_gen = input(
        "do you want to auto-generate a strong password? [y/n/q]: "
    )

    if ent_or_gen == "y":
        password = pwgenerator.generate()
        pyperclip.copy(password)
        print(
            f"{colors.OKGREEN}password copied to clipboard{colors.ENDC}"
        )
    elif ent_or_gen == "n":
        password = getpass(
            "enter the password: "
        )
        c_password = getpass(
            "confirm the password: "
        )

        if password == c_password:
            pass
        else:
            print(
                f"{colors.WARNING}passwords do not match{colors.ENDC}"
            )
            password = getpass(
                "enter the password: "
            )
            c_password = getpass(
                "confirm the password: "
            )

            if password == c_password:
                pass
            else:
                print(
                    f"{colors.FAIL}two failed attempts{colors.ENDC}"
                )
                quit()
    else:
        quit()

    cur.execute(
        """SELECT kdf_salt, ciphertext, nonce, auth_tag FROM passwords WHERE
        service_name=(?)""",
        (service_name,),
    )
    acc = cur.fetchone()

    if acc is not None:
        enc_password = encrypt_AES_GCM(
            password.encode("utf-8"), mpp
        )

        kdf_salt = enc_password[0]
        ciphertext = enc_password[1]
        nonce = enc_password[2]
        auth_tag = enc_password[3]

        cur.execute(
            """UPDATE passwords SET kdf_salt=? ,ciphertext=?, nonce=?,
            auth_tag=?, created_at=? WHERE service_name=? """,
            (
                kdf_salt,
                ciphertext,
                nonce,
                auth_tag,
                datetime.now(),
                service_name,
            ),
        )

        con.commit()
    else:
        print(
            f"{colors.WARNING}a record for the entered service does not exist{colors.ENDC}"
        )

    menu(mpp)


def get_info(mpp):
    service_name = input(
        "enter the name of the service: "
    )

    cur.execute(
        "SELECT identifier, service_url FROM passwords WHERE service_name=(?)",
        (service_name,),
    )
    data = cur.fetchone()

    if data is not None:
        print(
            f"{colors.OKBLUE}username:{colors.ENDC}\t{colors.OKGREEN}{data[0]}{colors.ENDC}\n{colors.OKBLUE}url:{colors.ENDC}\t\t{colors.OKGREEN}{data[1]}{colors.ENDC}"
        )
    else:
        print(
            f"{colors.WARNING}a record for the entered service does not exist{colors.ENDC}"
        )

    menu(mpp)


def show_help(mpp):
    print(
        f"""{colors.OKBLUE}init\t[in]{colors.ENDC}\t\t{colors.OKGREEN}initalize new database{colors.ENDC}
{colors.OKBLUE}add\t[a]{colors.ENDC}\t\t{colors.OKGREEN}add new password{colors.ENDC}
{colors.OKBLUE}read\t[r]{colors.ENDC}\t\t{colors.OKGREEN}read a password{colors.ENDC}
{colors.OKBLUE}update\t[u]{colors.ENDC}\t\t{colors.OKGREEN}update existing password{colors.ENDC}
{colors.OKBLUE}info\t[i]{colors.ENDC}\t\t{colors.OKGREEN}get info associated with the password{colors.ENDC}
{colors.OKBLUE}help\t[h]{colors.ENDC}\t\t{colors.OKGREEN}shows this help message{colors.ENDC}"""
    )

    menu(mpp)
