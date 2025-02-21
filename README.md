# Object-Oriented Programming (OOP) Principles

Object-Oriented Programming (OOP) is a paradigm that structures software design around objects rather than functions and logic. OOP helps improve code reusability, scalability, and maintainability. This document covers the core principles of OOP and the SOLID principles.

## Core Principles of OOP

### 1. Encapsulation
Encapsulation is the practice of bundling data (variables) and methods that operate on the data into a single unit, usually a class. It restricts direct access to some components and protects the integrity of the object.

```python
class Car:
    def __init__(self, brand, model):
        self.__brand = brand  # Private variable
        self.__model = model  # Private variable

    def get_car_info(self):
        return f"{self.__brand} {self.__model}"

car = Car("Toyota", "Corolla")
print(car.get_car_info())  # Toyota Corolla
```

### 2. Inheritance
Inheritance allows a class (child) to inherit attributes and methods from another class (parent), promoting code reusability.

```python
class Vehicle:
    def __init__(self, brand):
        self.brand = brand
    
    def drive(self):
        return "Driving..."

class Car(Vehicle):
    def __init__(self, brand, model):
        super().__init__(brand)
        self.model = model

car = Car("Toyota", "Camry")
print(car.brand)  # Toyota
print(car.drive())  # Driving...
```

### 3. Polymorphism
Polymorphism allows different classes to be treated as instances of the same class through a shared interface. This enables methods to be used interchangeably.

```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

animals = [Dog(), Cat()]
for animal in animals:
    print(animal.speak())
```

### 4. Abstraction
Abstraction is the process of hiding the internal details of an implementation and only exposing relevant functionalities. It helps in reducing complexity by allowing the user to interact with an object at a high level without needing to understand its internal workings.

In Python, abstraction is typically implemented using abstract classes and methods.
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        """This method must be implemented by subclasses."""
        pass

class Dog(Animal):
    def make_sound(self):
        return "Bark"

class Cat(Animal):
    def make_sound(self):
        return "Meow"

# Cannot instantiate an abstract class
# animal = Animal()  # This would raise an error

dog = Dog()
print(dog.make_sound())  # Bark
```

By using abstraction, we enforce a contract that subclasses must follow, ensuring consistency and structure in the codebase.

---

## SOLID Principles
The SOLID principles are five design principles that help improve software maintainability and scalability.

### 1. Single Responsibility Principle (SRP)
A class should have only one reason to change, meaning it should have only one job.

```python
class ReportGenerator:
    def generate(self):
        return "Report data"

class ReportPrinter:
    def print_report(self, report):
        print(report)

report = ReportGenerator().generate()
ReportPrinter().print_report(report)
```

### 2. Open/Closed Principle (OCP)
Entities should be open for extension but closed for modification.

```python
from abc import ABC, abstractmethod

class Discount(ABC):
    @abstractmethod
    def apply_discount(self, price):
        pass

class PercentageDiscount(Discount):
    def apply_discount(self, price):
        return price * 0.9  # 10% off

class FixedDiscount(Discount):
    def apply_discount(self, price):
        return price - 10

pricing = PercentageDiscount()
print(pricing.apply_discount(100))  # 90.0
```

### 3. Liskov Substitution Principle (LSP)
Subtypes must be substitutable for their base types without altering the correctness of the program.

```python
class Bird:
    def fly(self):
        return "Flying"

class Penguin(Bird):
    def fly(self):
        raise Exception("Penguins can't fly")

# Violates LSP because Penguin cannot fully replace Bird
```

### 4. Interface Segregation Principle (ISP)
Clients should not be forced to depend on interfaces they do not use.

```python
class Printer:
    def print(self):
        pass

class Scanner:
    def scan(self):
        pass

class MultiFunctionPrinter(Printer, Scanner):
    def print(self):
        return "Printing..."

    def scan(self):
        return "Scanning..."
```

### 5. Dependency Inversion Principle (DIP)
High-level modules should not depend on low-level modules. Both should depend on abstractions.

```python
class Database(ABC):
    @abstractmethod
    def connect(self):
        pass

class MySQLDatabase(Database):
    def connect(self):
        return "Connected to MySQL"

class App:
    def __init__(self, database: Database):
        self.database = database
    
    def start(self):
        return self.database.connect()

app = App(MySQLDatabase())
print(app.start())  # Connected to MySQL
```

---

## Conclusion
Understanding and applying OOP principles and the SOLID design principles can help developers create robust, maintainable, and scalable applications. By leveraging encapsulation, inheritance, polymorphism, and abstraction, alongside SOLID principles, you can write clean, efficient, and modular code.

---


