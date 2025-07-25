import sys
import segno
from tqdm import tqdm
import time

import secrets
import base64
import hmac
import hashlib
import struct


# ========= function for generating a secret ========
def generate_shared_secret():
    return secrets.token_bytes(10)


# ========= function for generating the QR code ========
def gen_qr(user_id):
    # Example URI: otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example
    code1 = "otpauth://totp/Google%20Authenticator:"
    code2 = "?secret="
    code3 = "&issuer=Google%20Authenticator"

    secret = base64.b32encode(generate_shared_secret()).decode('utf-8')     # generate secret key
    
    # TODO: combine code# and user id to create URI (hint: match example URI format given above)
    uri = code1+user_id+code2+secret+code3
    print(" >> URI generated: ", uri)

    # TODO: store secret into a file named "secret.txt"
    file = open("secret.txt", "w")
    file.write(secret)
    file.close()

    # TODO: generate QR code based on the URI using snego library
    qrcode = segno.make(uri, micro=False)
    qrcode.save('qr_code.png')

    return


# ========= function for generating the One-Time Password ========
def generate_otp(secret_base32, digits=6, time_step=30):
    # decode the base32-encoded secret string into raw bytes
    key = base64.b32decode(secret_base32, casefold=True)

    # TODO: get the current time step
    current_time = int(time.time())
    counter = current_time // time_step
    # convert the counter to an 8-byte big-endian byte array
    counter_bytes = struct.pack(">Q", counter)

    # create an HMAC-SHA1 hash using the secret key and the counter
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    # the dynamic offset is the last nibble (4 bits) of the HMAC
    # this chooses where to start slicing the hash
    offset = hmac_hash[-1] & 0x0F       # value between 0 and 15

    # TODO: take 4 bytes of hmac hash starting at the offset
    selected_bytes = hmac_hash[offset:offset+4]

    # convert those 4 bytes to a big-endian integer
    code_int = struct.unpack(">I", selected_bytes)[0]

    # TODO: remove the sign bit; Hint: 0x7FFFFFFF = 0111 1111 1111 1111 1111 1111 1111 1111
    code_int = code_int & 0x7FFFFFFF 

    # TODO: get only 6 digits; Hint: mod 10^?
    otp = code_int % 10**6

    return otp


# ========= function for displaying OPT every 30 sec ========
def get_otp(t=30):
    # TODO: open and read file containing secret; Hint: use readline
    file = open("secret.txt", "r")
    secret = file.readline().strip()  # read the secret from the file and remove any whitespace
    file.close()

    while True:
        # Calculează cât timp a mai rămas până la următorul interval de 30 secunde
        seconds_left = int(t - (time.time() % t))
        otp = generate_otp(secret)
        print(" > Generated OTP:", otp, "valid for", seconds_left, "seconds")
        # Așteaptă până la următorul interval de 30 secunde
        for _ in tqdm(range(seconds_left, 0, -1), desc="Loading…", ascii=False, ncols=75):
            time.sleep(1)


# ========= mainfunction for command handling ========
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(" >> Invalid flag: can either be \"--generate-qr [user_id]\" or \"--get-otp\"")
    elif sys.argv[1] == "--generate-qr" and len(sys.argv) == 3:
        gen_qr(sys.argv[2])
    elif sys.argv[1] == "--get-otp" and len(sys.argv) == 2:
        get_otp()
    else:
        print(" >> Invalid flag: can either be \"--generate-qr [user_id]\" or \"--get-otp\"")
