from getpass import getpass
from encdec import encrypt_AES_GCM, decrypt_AES_GCM
from menu import menu, create_pass, read_pass


mp = (
    b"Q\xa1\x0fe\xbe\xcb\xfb\xe1J:5T-\x913\xd7",
    b"C\x11'oS\xbd'\x1a\xd6!\x03\xa2\x91yu\x8f\xec\xbf\xbc!\x18",
    b"7Kw\xd8\x15\xf5\x11\xc0\xc8\x07\xca\xc2\x9fW'\xf2",
    b"Z\xb8B6\xe44[\x04\xc7\xa4\x92$\xc3F\xb6\xdb",
)
mpp = getpass("Enter master password: ").encode("utf-8")

try:
    masterPass = decrypt_AES_GCM(mp, mpp)
except:
    print("fuck off!")
    quit()

print("welcome!")
menu(mpp)
