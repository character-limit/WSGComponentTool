import sqlite3
import bcrypt
from user import User


class UserDB:

    def __init__(self):
        self.conn = sqlite3.connect("users.db") #connect to db file
        self.create_table()   

    def create_table(self): #create users table if its not already existing
        self.conn.execute("""CREATE TABLE IF NOT EXISTS users (
                    firstName TEXT,
                    lastName TEXT,
                    password TEXT,
                    admin BOOLEAN,
                    username TEXT UNIQUE,
                    UID TEXT UNIQUE
                    )""")
        self.conn.commit()

    def add_user(self, user: User): #add user obj to db
        #? and tuple to prevent SQL injection
        self.conn.execute("INSERT INTO users (firstName, lastName, password, admin, username, UID) VALUES (?, ?, ?, ?, ?, ?)", (user.firstName, user.lastName, user.password, int(user.isAdmin), user.username, self.gen_UID()))
        self.conn.commit()

    def get_user(self, username) -> User | None:
        cursor = self.conn.cursor()

        #select the user with the matching username
        cursor.execute("SELECT firstName, lastName, password, UID, admin, username FROM users WHERE username = ?", (username,))
        
        row = cursor.fetchone()
        if row: #if user found, create and return obj - index is in order of select statement.
            return User(row[0], row[1], row[5], row[2], row[3], bool(row[4]))
        return None #ret none if not found
    
    def get_users(self):
        cursor = self.conn.cursor()

        #select the item with the matching ID or name
        cursor.execute("SELECT firstName, lastName, password, UID, admin, username FROM users ")
        
        rows = cursor.fetchall()
        if rows: #if item found, create and return obj - index is in order of select statement.
            return [User(row[0], row[1], row[5], row[2], row[3], bool(row[4])) for row in rows]
        return None #ret none if not found

    #check usename and password, return boolean for success
    def check_login(self, username, password) -> int:
        try:
            user = self.get_user(username)
            #if exists and password matches
            if user and user.check_password(password):
                User.session = user
                return 1
            return 0
        except Exception:
            return -1

    def edit_user(self, user: User): #edit existing user
        #? and tuple to prevent SQL injection
        self.conn.execute("UPDATE users SET firstName = ?, lastName = ?, password = ?, admin = ? WHERE username = ?", (user.firstName, user.lastName, user.password, int(user.isAdmin), user.username))
        self.conn.commit()

    #gen unique uid for new user
    def gen_UID(self) -> str:

        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(UID) FROM users") #get highest uid to +1

        row = cursor.fetchone()
        if row[0] is None: #if no users yet
            return "0001"
        
        temp = int(row[0]) + 1 #get last uid +=1
        return str(temp).zfill(4) #convert int to str with leading 0 for storage