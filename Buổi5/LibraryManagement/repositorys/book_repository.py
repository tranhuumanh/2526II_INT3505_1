from week5.LibraryManagement.data.book_database import books, Book


def get_all_books():
    return books


def find_book_by_id(id):
    for b in books:
        if b.id == id:
            return b
    return None


def add_book(book):
    books.append(book)


def update_book(id, title=None, author=None):
    for i, b in enumerate(books):
        if b.id == id:
            books[i] = Book(
                id, title if title else b.title, author if author else b.author
            )
            return books[i]
    return None


def delete_book(id):
    for i, b in enumerate(books):
        if b.id == id:
            books.pop(i)
            return True
    return False
