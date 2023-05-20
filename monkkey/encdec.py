import binascii
import os

import scrypt
from Crypto.Cipher import AES


def encrypt_AES_GCM(msg, password):
    kdfSalt = os.urandom(16)
    secretKey = scrypt.hash(
        password,
        kdfSalt,
        N=16384,
        r=8,
        p=1,
        buflen=32,
    )
    aesCipher = AES.new(
        secretKey, AES.MODE_GCM
    )
    (
        ciphertext,
        authTag,
    ) = aesCipher.encrypt_and_digest(msg)
    return (
        kdfSalt,
        ciphertext,
        aesCipher.nonce,
        authTag,
    )


def decrypt_AES_GCM(encryptedMsg, password):
    (
        kdfSalt,
        ciphertext,
        nonce,
        authTag,
    ) = encryptedMsg
    secretKey = scrypt.hash(
        password,
        kdfSalt,
        N=16384,
        r=8,
        p=1,
        buflen=32,
    )
    aesCipher = AES.new(
        secretKey, AES.MODE_GCM, nonce
    )
    plaintext = (
        aesCipher.decrypt_and_verify(
            ciphertext, authTag
        )
    )
    return plaintext
