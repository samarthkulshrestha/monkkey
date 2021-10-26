from encdec import encrypt_AES_GCM

def set_new_master_password(mpp):
    enc_master_pass = encrypt_AES_GCM(mpp, mpp)

    with open("master.py", "w") as file:
        file.write(f"mp = {enc_master_pass}")

