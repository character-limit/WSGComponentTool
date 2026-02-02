import sqlite3
from Main.audit import Audit
from Main.user import User


class AuditDB:

    def __init__(self):
        self.conn = sqlite3.connect("audit.db") #connect to db file
        self.create_table()   

    def create_table(self): #create users table if its not already existing
        self.conn.execute("""CREATE TABLE IF NOT EXISTS audit (
                    description TEXT,
                    timestamp TEXT,
                    userID TEXT
                    )""")
        self.conn.commit()

    def add_audit(self, audit: Audit): #add audit obj to db
        #? and tuple to prevent SQL injection
        self.conn.execute("INSERT INTO audit (description, timestamp, userID) VALUES (?, ?, ?)", (audit.description, audit.timestamp, audit.userID))
        self.conn.commit()

    """ def get_audit(self, userID) -> User | None:
        cursor = self.conn.cursor()

        #select the user with the matching username
        cursor.execute("SELECT description, timestamp, userID FROM audit WHERE userID = ?", (userID,))
        
        row = cursor.fetchone()
        if row: #if user found, create and return obj - index is in order of select statement.
            return Audit(row[0], row[1], row[2])
        return None #ret none if not found """
    
    def get_audits(self):
        cursor = self.conn.cursor()

        #select the item with the matching ID or name
        cursor.execute("SELECT description, timestamp, userID FROM audit")
        
        rows = cursor.fetchall()
        if rows: #if item found, create and return obj - index is in order of select statement.
            return [Audit(row[0], row[1], row[2]) for row in rows]
        return None #ret none if not found