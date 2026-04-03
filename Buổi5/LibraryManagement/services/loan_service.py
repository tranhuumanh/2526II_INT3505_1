from repositorys import loan_repository


# Cursor-based pagination
def get_loans(last_id=None, size=5):
    loans = loan_repository.get_all_loans()
    loans_sorted = sorted(loans, key=lambda x: x.id)  # sắp xếp theo id
    start_index = 0
    if last_id:
        for i, l in enumerate(loans_sorted):
            if l.id == last_id:
                start_index = i + 1
                break
    return {
        "loans": loans_sorted[start_index : start_index + size],
        "next_cursor": (
            loans_sorted[start_index + size - 1].id
            if start_index + size - 1 < len(loans_sorted)
            else None
        ),
    }


def create_loan(data):
    loan = loan_repository.find_loan_by_id(data["id"])
    if loan:
        return None
    from week5.LibraryManagement.data.loan_database import Loan

    new_loan = Loan(
        data["id"],
        data["user_id"],
        data["book_id"],
        data["loan_date"],
        data.get("return_date"),
    )
    loan_repository.add_loan(new_loan)
    return new_loan


def update_loan(id, data):
    return loan_repository.update_loan(
        id,
        user_id=data.get("user_id"),
        book_id=data.get("book_id"),
        loan_date=data.get("loan_date"),
        return_date=data.get("return_date"),
    )


def delete_loan(id):
    return loan_repository.delete_loan(id)


def find_loan(id):
    return loan_repository.find_loan_by_id(id)
