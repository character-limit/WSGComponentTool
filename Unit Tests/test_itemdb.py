import unittest
import Main.itemdb as itemdb
from Main.item import Item

class TestItemDBMethods(unittest.TestCase):

    #test adding an item to the db and retrieving it.
    def test_add_item(self):
        db = itemdb.ItemDB(":memory:")
        item = Item("Item123", "Shelf A", 67)

        db.add_item(item)
        check = db.get_item(item.ID)

        self.assertIsNotNone(check)
        self.assertEqual(check.name, "Item123")
        self.assertEqual(check.quantity, 67)

    #test removing an item from the db
    def test_remove_item(self):
        db = itemdb.ItemDB(":memory:")
        item = Item("Item123", "Shelf A", 67)

        db.add_item(item)
        check1 = db.get_item(item.ID)
        db.remove_item(item.ID)
        check2 = db.get_item(item.ID)

        self.assertIsNotNone(check1)
        self.assertIsNone(check2)

    #test getting an item from the db
    def test_get_item(self):
        db = itemdb.ItemDB(":memory:")
        item = Item("Item123", "Shelf A", 67)

        db.add_item(item)
        check = db.get_item(item.ID)

        self.assertIsNotNone(check)
        self.assertEqual(check.name, "Item123")
        self.assertEqual(check.quantity, 67)

    #test searching for items in the db
    def test_search_items(self):
        db = itemdb.ItemDB(":memory:")
        item1 = Item("Item123", "Shelf A", 67)
        item2 = Item("Item321", "temp A", 69)

        db.add_item(item1)
        db.add_item(item2)
        results = db.get_items("Item")
        results2 = db.get_items("temp")

        self.assertIsNotNone(results)
        self.assertEqual(len(results), 2)
        self.assertIsNotNone(results2)
        self.assertEqual(len(results2), 1)
        self.assertEqual(results2[0].name, "Item321")

if __name__ == '__main__':
    unittest.main()