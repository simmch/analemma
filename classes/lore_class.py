import utilities.database as db

class Lore:
    def __init__(self, title, description, writer, timestamp):
        self.title = title
        self.description = description
        self.writer = writer
        self.timestamp = timestamp
    
    def save(self):
        return db.save_lore(self.__dict__)