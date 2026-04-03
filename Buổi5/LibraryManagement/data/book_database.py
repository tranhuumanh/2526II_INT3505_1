class Book:
    def __init__(self, id, title, author):
        self.id = id
        self.title = title
        self.author = author

    def to_dict(self):
        return {"id": self.id, "title": self.title, "author": self.author}


books = [
    Book("1", "Learn Python", "Author A"),
    Book("2", "Data Structures", "Author B"),
    Book("3", "Algorithms", "Author C"),
    Book("4", "Database Systems", "Author D"),
    Book("5", "Operating Systems", "Author E"),
]
