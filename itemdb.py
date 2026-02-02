import sqlite3
from item import Item


class ItemDB:

    def __init__(self, path="items.db"):
        self.conn = sqlite3.connect(path) #connect to db file
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
        
        item.ID = cursor.lastrowid #set item ID to new one (next incremented value), index provided by db.
        self.conn.commit()  #save changes
        return item #return item with given ID.
    
    def remove_item(self, itemID): #add item obj to db
        cursor = self.conn.cursor()
        #? and tuple to prevent SQL injection
        self.conn.execute("DELETE FROM items WHERE ID = ?", (itemID,))
        self.conn.commit()
        return cursor.rowcount >0
    
    def edit_item(self, item: Item): #edit existing item
        #? and tuple to prevent SQL injection
        self.conn.execute("UPDATE items SET name = ?, location = ?, quantity = ?, minQuantity = ? WHERE ID = ?", (item.name, item.location, item.quantity, item.minQuantity, item.ID))
        self.conn.commit()

    def get_items(self, term):
        cursor = self.conn.cursor()
        term = f"%{term}%" #wildcard characters surrounding search term, to allow for LIKE operator to search within the strings.

        #select the item with matching ID or name or loci
        cursor.execute("SELECT name, location, quantity, ID, minQuantity FROM items WHERE name LIKE ? OR location LIKE ? OR ID LIKE ?", (term, term, term))
        
        rows = cursor.fetchall() #fetch all matching rows

        if rows: #if item(s) found, create and return obj - index is in order of select statement.
            return [Item(row[0], row[1], row[2], row[3], row[4]) for row in rows] #return list of items.
        return None #ret none if not found
    
    def get_items_monitoring(self, lowStockOnly = False):
        cursor = self.conn.cursor()

        #select the item with the matching ID or name
        if lowStockOnly:
            cursor.execute("SELECT name, location, quantity, ID, minQuantity FROM items WHERE quantity <= minQuantity AND minQuantity != -1")
        else:
            cursor.execute("SELECT name, location, quantity, ID, minQuantity FROM items WHERE minQuantity != -1")
        
        rows = cursor.fetchall()
        if rows: #if item found, create and return obj - index is in order of select statement.
            return [Item(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        return None #ret none if not found
    
    def get_item(self, ID):
        cursor = self.conn.cursor()

        #select the item with the matching ID
        cursor.execute("SELECT name, location, quantity, ID, minQuantity FROM items WHERE ID = ?", (ID,))
        
        row = cursor.fetchone()
        if row: #if item found, create and return obj - index is in order of select statement.
            return Item(row[0], row[1], row[2], row[3], row[4])
        return None #ret none if not found