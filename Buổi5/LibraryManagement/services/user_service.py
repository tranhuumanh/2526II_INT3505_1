from repositorys import user_repository


# Page-based pagination
def get_users(page=None, size=None):
    users = user_repository.get_all_users()
    total = len(users)
    if page is not None and size is not None:
        offset = page * size
        users = users[offset : offset + size]
    return {"users": users, "total": total, "page": page, "size": size}


def create_user(data):
    return user_repository.create_user(data)


def update_user(id, data):
    return user_repository.update_user(
        id, data["name"], data["email"], data["password"]
    )


def delete_user(id):
    return user_repository.delete_user(id)


def find_user(id):
    return user_repository.find_user_by_id(id)


def login(email, password):
    return user_repository.login(email, password)
