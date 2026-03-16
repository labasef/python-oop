class User:
    def __init__(self, username, password):
        self.username = username
        self._password = password

    def __get_password(self):
        return "Cannot give the password out!"

    def __set_password(self, password):
        self._password = password

    def login(self, username, password):
        if username == self.username and password == self._password:
            print("Login successful!")
        else:
            print("Login failed!")

    # property() is a built-in function that creates and returns a property object
    password = property(__get_password, __set_password)


# Usage
user = User("user", "password")
user.login("user", "password")  # Output: Login successful!
user.password = "new_password"
print(user.password)  # Output: Cannot give the password out!
user.login("user", "password")  # Output: Login failed!
user.login("user", "new_password")  # Output: Login successful!

class A:
    def __init__(self):
        self.__x = 1


a = A()
print(a._A__x)  # Output: 1
a.__x = 2
print(a.__x)  # Output: 2
