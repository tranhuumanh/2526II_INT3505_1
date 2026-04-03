from repositorys import book_repository


# Offf limit pagination
def get_books(page=None, size=None):
    books = book_repository.get_all_books()
    if page is not None and size is not None:
        offset = page * size
        books = books[offset : offset + size]
    return books


def create_book(data):
    book = book_repository.find_book_by_id(data["id"])
    if book:
        return None
    from week5.LibraryManagement.data.book_database import Book

    new_book = Book(data["id"], data["title"], data["author"])
    book_repository.add_book(new_book)
    return new_book


def update_book(id, data):
    return book_repository.update_book(
        id, title=data.get("title"), author=data.get("author")
    )


def delete_book(id):
    return book_repository.delete_book(id)


def find_book(id):
    return book_repository.find_book_by_id(id)
