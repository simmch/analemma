import utilities.database as db

class Lore:
    def __init__(self, title, description, writer, timestamp, title_no_spaces, description_no_spaces):
        self.title = title_no_spaces
        self.description = description_no_spaces
        self.writer = writer
        self.timestamp = timestamp
        self.original_title = title
        self.original_description = description 
    
    def save(self):
        return db.save_lore(self.__dict__)