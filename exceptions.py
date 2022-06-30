class InvalidUser(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return f"{self.username} isn't a valid username."


class InactiveUser(Exception):
    def __str__(self):
        return f"You do not have enough activity on your Twitter profile."


class ApiError(Exception):
    def __str__(self):
        return "Something went wrong with the API."
