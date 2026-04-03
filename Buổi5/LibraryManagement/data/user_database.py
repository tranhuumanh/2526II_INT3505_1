class User:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }


users = [
    User("1", "Ton Thien Khoe", "khoe@gmail.com", "password1"),
    User("2", "Nguyen Van A", "vana@gmail.com", "password2"),
]
