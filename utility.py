import hashlib, binascii, os

def hash_password(password):
    #Hash a password for storing
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    hashed_password = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    hashed_password = binascii.hexlify(hashed_password)
    return (salt + hashed_password).decode('ascii')

#creates a new password
def create_password(check=None):
    password1 = ''
    password2 = ' '
    while password1 != password2:
        password1 = input("Enter your new password>> ")
        while password1 == '':
            password1 = input("Enter your new password>> ")
        password2 = input('Confirm password>> ')
        while password2 == '':
            password2 = input('Confirm password>> ')
        if password1 != password2:
            print("Passwords do not match")
    
       
    return hash_password(password1)

