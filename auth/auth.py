class Authentication:
    USERS = [{"username": "user1",
              "password": "pwd1"}]

    def login(self, username, password):
        u = self.fetch_user(username)
        if not u or u["password"] != password:
            return None
        return u

    def fetch_user(self, username):
        for u in self.USERS:
            if u["username"] == username:
                return u
        else:
            return None


class Authorization:
    PERMISSIONS = [{"user": "user1",
                    "permissions": {"create", "edit", "delete"}}]

    def can(self, user, action):
        for u in self.PERMISSIONS:
            if u["user"] == user["username"]:
                return action in u["permissions"]
        else:
            return False
