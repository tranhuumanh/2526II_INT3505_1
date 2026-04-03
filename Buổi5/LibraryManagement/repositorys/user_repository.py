from week5.LibraryManagement.data.user_database import users, User


def get_all_users():
    return users


def find_user_by_id(id):
    for u in users:
        if u.id == id:
            return u
    return None


def add_user(user):
    users.append(user)


def update_user(id, name, email):
    for i, u in enumerate(users):
        if u.id == id:
            users[i] = User(id, name, email)
            return users[i]
    return None


def delete_user(id):
    for i, u in enumerate(users):
        if u.id == id:
            users.pop(i)
            return True
    return False


def login(email, password):
    for u in users:
        if u.email == email and u.password == password:
            return u
    return None


def create_user(data):

    # kiểm tra id đã tồn tại chưa
    for user in users:
        if user.id == data["id"]:
            return None

    # nếu chưa tồn tại thì tạo user
    user = User(data["id"], data["name"], data["email"], data)
    add_user(user)

    return user
