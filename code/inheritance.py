class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self):
        pass


class Dog(Animal):
    def speak(self):
        return "Woof!"


class Cat(Animal):
    def speak(self):
        return "Meow!"


class Human(Animal):
    def __init__(self, name: str, job: str):
        super().__init__(name)
        self.job = job  # New attribute

    def speak(self):
        return "Hello!"

    def work(self):
        return f"Working {self.job}"


# Usage
dog = Dog("Rex")
print(dog.speak())  # Output: Woof!

cat = Cat("Tom")
print(cat.speak())  # Output: Meow!

human = Human("Bob", "Developer")
print(human.speak())  # Output: Hello!
print(human.work())  # Output: Working Developer

