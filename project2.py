import re, os, os.path, pickle, utility, hashlib, binascii

class BasePasswordManager():

    #stores all the passwords
    old_passwords = []
    
    #Function returns current passowrd
    def get_password(self):

        #checks if file exists
        if os.path.isfile("passwords.txt"):

            #if the file exists it opens the file to read it
            with open('passwords.txt', 'rb') as myFile:
                self.old_passwords = pickle.load(myFile) #return a list with all old passwords
                reversed_password = self.old_passwords[::-1] #reverses the list of old passwords
                return reversed_password[0] #returns current password

        #if the file doesn't exist it returns a character as the current password
        else:
            return False

    def is_correct(self, provided_password):
        #Verify a stored password against one provided by user
        stored_password = self.get_password()
        salt = stored_password[:64]  
        stored_password = stored_password[64:]
        hashed_password = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
        hashed_password = binascii.hexlify(hashed_password).decode('ascii')
        return hashed_password == stored_password

    
class PasswordManager(BasePasswordManager):

    #initializes values
    def __init__(self, password=''):
        self.password = password        #new password that will be entered
    
    #Function sets password
    def  set_password(self):
        current_password = self.get_password()    #gets current passowrd in the old_password list
        current_password_level = self.get_level(current_password)    #gets level of current password thats in the list
        new_password_level = self.get_level(self.password)   #gets level of new password entered 
        
        #checks if new password's level is greater than current passowrd
        if new_password_level >= current_password_level:

            #checks if new password's length is greater or equal to 6
            if len(self.password) >= 6:

                #opens a file to write and save new password
                with open('passwords.txt', 'wb') as myFile:
                    password_list = self.old_passwords 
                    password_list.append(self.password) #appends new password into the list
                    pickle.dump(password_list, myFile) #saves old_password list into the file
                    print('Password saved')

                #if your new password is shorter than the current password
            else:
                print("Password is shorter than the last one, it must be equal or more than ", current_password)
        
        #if your new password's level is lower than the current password
        else:
            print("new password must be of the highest security level for a successful password change")
            
    #function gets level of a password and returns it
    def get_level(self, password):
        regexp = re.compile('[^0-9a-zA-Z]+')

        if password == False:
            return 0
        #level 1
        elif password.isalpha():
            return 1
        #level 2
        elif password.isalnum():
            return 2
        #level 3
        elif regexp.search(password):
            return 3
        

PasswordManager_object = BasePasswordManager()
if PasswordManager_object.get_password() == False:
    #create_password() is a method from the utility module
    new_password = utility.create_password()
    PasswordManager_object = PasswordManager(new_password)
    PasswordManager_object.set_password()

else:
    has_error = True
    while has_error:
        prev_password = input('Enter the previous password>> ')
        prev_password = PasswordManager_object.is_correct(prev_password)
        while  prev_password != True:
            print('Entered password does not match the one on the system')
            prev_password = input('Enter the correct previous password in order to change it>> ')
            prev_password = PasswordManager_object.is_correct(prev_password)
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

        #hash_password() is a method from the utility module, it encrypts the new password
        password1 = utility.hash_password(password1) #hash new password
        PasswordManager_object = PasswordManager(password1)
        PasswordManager_object.set_password()
        has_error = False