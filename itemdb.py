import sqlite3
from item import Item


class ItemDB:

    def __init__(self):
        self.conn = sqlite3.connect("items.db") #connect to db file
        self.create_table()   

    def create_table(self): #create item table if its not already existing
        self.conn.execute("""CREATE TABLE IF NOT EXISTS items (
                    name TEXT,
                    location TEXT,
                    quantity INTEGER,
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    minQuantity INTEGER
                    )""")
        self.conn.commit()

    def add_item(self, item): #add item obj to db
        #? and tuple to prevent SQL injection
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO items (name, location, quantity, minQuantity) VALUES (?, ?, ?, ?)", (item.name, item.location, item.quantity, item.minQuantity))
        
        item.ID = cursor.lastrowid #set item ID to new one genned by sql
        self.conn.commit()
        return item

    def get_items(self, term):
        cursor = self.conn.cursor()
        term = f"%{term}%"

        #select the item with the matching ID or name
        cursor.execute("SELECT name, location, quantity, ID, minQuantity FROM items WHERE name LIKE ? OR location LIKE ? OR ID LIKE ?", (term, term, term))
        
        rows = cursor.fetchall()
        if rows: #if item found, create and return obj - index is in order of select statement.
            return [Item(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        return None #ret none if not found