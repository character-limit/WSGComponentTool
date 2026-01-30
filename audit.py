import datetime

class Audit:

    def __init__(self, description, timestamp, userID):
        self.description = description
        self.timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        self.userID = userID


    def __repr__(self):
        return f"Audit(description={self.description}, timestamp={self.timestamp}, userID={self.userID})"