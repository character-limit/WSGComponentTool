import bcrypt

class User:

    #current user session obj
    session = None

    def __init__(self, firstName, lastName, username, password, UID=None, isAdmin=False):
        self.firstName = firstName.title() #correctly format names and usernames
        self.lastName = lastName.title()
        self.username = username.lower()

        #hash password if not already hashed
        if isinstance(password, bytes):#hash password if not already hashed
            self.password = password
        else:
            self.password = self._hash_password(password)

        self.UID = UID
        self.isAdmin = isAdmin

    def __repr__(self):
        return f"User(name={self.firstName} {self.lastName}, username={self.username}, password={self.password}, UID={self.UID})"

    #internal func to hash pass
    def _hash_password(self, password):
        return bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()) #hash plaintext pwd
    
    #check param password against stored hashed password in provided user obj
    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password)