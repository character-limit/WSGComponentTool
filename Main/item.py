class Item:

    def __init__(self, name, location, quantity, ID = None, minQuantity=-1):#min -1 if not provided, used to show NO stock alert..
        self.name = name.title() #title these fields for consistency
        self.location = location.title()
        self.quantity = quantity
        self.ID = ID
        self.minQuantity = minQuantity

    def __repr__(self):
        return f"Item(name={self.name}, location={self.location}, quantity={self.quantity}, ID={self.ID}, minQuantity={self.minQuantity})"