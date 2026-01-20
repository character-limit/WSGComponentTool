import sqlite3
import bcrypt
from user import User


class UserDB:

    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.create_table()

    def create_table(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS users (
                    firstName TEXT,
                    lastName TEXT,
                    password TEXT,
                    admin BOOLEAN,
                    username TEXT UNIQUE,
                    UID TEXT UNIQUE
                    )""")
        self.conn.commit()

    def add_user(self, user: User):
        #? and tuple to prevent SQL injection
        self.conn.execute("INSERT INTO users (firstName, lastName, password, admin, username, UID) VALUES (?, ?, ?, ?, ?, ?)", (user.firstName, user.lastName, user.password, int(user.isAdmin), user.username, user.UID))
        self.conn.commit()

    def get_user(self, username) -> User | None:
        cursor = self.conn.cursor()

        cursor.execute("SELECT firstName, lastName, password, UID, admin, username FROM users WHERE username = ?", (username,))
        
        row = cursor.fetchone()
        if row:
            return User(row[0], row[1], row[5], row[2], row[3], bool(row[4]))
        
        return None
    
    def check_login(self, username, password) -> bool:
        user = self.get_user(username)
        print(user)
        if user and user.check_password(password):
            User.session = user
            return True
        return False

    def gen_UID(self) -> str:

        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(UID) FROM users")

        row = cursor.fetchone()
        if row[0] is None:
            return "0001"
        
        temp = int(row[0]) + 1 #get last uid +=1
        return str(temp).zfill(4) #convert int to str with leading 0 for storage