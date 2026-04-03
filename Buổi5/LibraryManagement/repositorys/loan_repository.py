from week5.LibraryManagement.data.loan_database import loans, Loan


def get_all_loans():
    return loans


def find_loan_by_id(id):
    for l in loans:
        if l.id == id:
            return l
    return None


def add_loan(loan):
    loans.append(loan)


def update_loan(id, user_id=None, book_id=None, loan_date=None, return_date=None):
    for i, l in enumerate(loans):
        if l.id == id:
            loans[i] = Loan(
                id,
                user_id if user_id else l.user_id,
                book_id if book_id else l.book_id,
                loan_date if loan_date else l.loan_date,
                return_date if return_date else l.return_date,
            )
            return loans[i]
    return None


def delete_loan(id):
    for i, l in enumerate(loans):
        if l.id == id:
            loans.pop(i)
            return True
    return False
