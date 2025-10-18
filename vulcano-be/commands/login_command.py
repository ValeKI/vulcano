class LoginCommand:
    def __init__(self, usernameOrEmail: str, password: str):
        self.usernameOrEmail = usernameOrEmail
        self.password = password

    @classmethod
    def from_dict(cls, data: dict):
        usernameOrEmail = data.get("usernameOrEmail")
        password = data.get("password")
        if not usernameOrEmail or not password:
            raise ValueError("Missing user, email or password")
        return cls(usernameOrEmail, password)