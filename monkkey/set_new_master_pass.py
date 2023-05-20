import pickle

from encdec import encrypt_AES_GCM


def set_new_master_password(mpp):
    enc_master_pass = encrypt_AES_GCM(
        mpp, mpp
    )
    pickle.dump(
        enc_master_pass,
        open("master.txt", "wb"),
    )

    print(
        "new master password set, please login again"
    )
