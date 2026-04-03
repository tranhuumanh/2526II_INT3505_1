class Loan:
    def __init__(self, id, user_id, book_id, loan_date, return_date=None):
        self.id = id
        self.user_id = user_id  # tham chiếu bằng id
        self.book_id = book_id  # tham chiếu bằng id
        self.loan_date = loan_date
        self.return_date = return_date

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "loan_date": self.loan_date,
            "return_date": self.return_date,
        }


loans = [
    Loan("1", "1", "1", "2026-04-01"),
    Loan("2", "2", "2", "2026-04-02"),
]
