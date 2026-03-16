# SOLID Principles

## Learning Objectives

By the end of this section, you should understand:
- How to design classes with a single responsibility
- When to use inheritance vs. composition
- How to create flexible, extensible code
- The importance of proper dependency management
- How to design cohesive interfaces

---

The SOLID principles are five design principles that help improve software maintainability and scalability.

## 1. Single Responsibility Principle (SRP)
A class should have only one reason to change, meaning it should have only one job.

```mermaid
classDiagram
    class ReportGenerator {
        +generate() String
    }
    class ReportPrinter {
        +print_report(report)
    }
    ReportGenerator ..> ReportPrinter : uses
```

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

## 2. Open/Closed Principle (OCP)
Entities should be open for extension but closed for modification.

```mermaid
classDiagram
    class Discount {
        <<abstract>>
        +apply_discount(price)* float
    }
    Discount <|-- PercentageDiscount
    Discount <|-- FixedDiscount
    class PercentageDiscount {
        +apply_discount(price) float
    }
    class FixedDiscount {
        +apply_discount(price) float
    }
```

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

## 3. Liskov Substitution Principle (LSP)
Subtypes must be substitutable for their base types without altering the correctness of the program.

```mermaid
classDiagram
    class Bird {
        +fly() String
    }
    Bird <|-- Sparrow
    Bird <|-- Penguin
    class Sparrow {
        +fly() String
    }
    class Penguin {
        +fly() ❌ raises Exception
    }
    note for Penguin "Violates LSP — cannot substitute Bird"
```

```python
class Bird:
    def fly(self):
        return "Flying"

class Penguin(Bird):
    def fly(self):
        raise Exception("Penguins can't fly")

# Violates LSP because Penguin cannot fully replace Bird
```

## 4. Interface Segregation Principle (ISP)
Clients should not be forced to depend on interfaces they do not use.

```mermaid
classDiagram
    class Printer {
        +print()
    }
    class Scanner {
        +scan()
    }
    Printer <|-- MultiFunctionPrinter
    Scanner <|-- MultiFunctionPrinter
    class MultiFunctionPrinter {
        +print()
        +scan()
    }
```

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

## 5. Dependency Inversion Principle (DIP)
High-level modules should not depend on low-level modules. Both should depend on abstractions.
You should depend on abstractions, not on concretions. This allows you to easily swap out implementations without changing the high-level code.

```mermaid
classDiagram
    class Database {
        <<abstract>>
        +connect()* String
    }
    Database <|-- MySQLDatabase
    Database <|-- PostgreSQLDatabase
    App --> Database : depends on abstraction
    class MySQLDatabase {
        +connect() String
    }
    class PostgreSQLDatabase {
        +connect() String
    }
    class App {
        -Database database
        +start() String
    }
```

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

## ⚠️ Anti-Patterns to Avoid

### 1. God Object (Violates SRP)
**Problem**: A class that does too much

```python
# ❌ Bad: User class handling too many responsibilities
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def save_to_database(self):
        pass
    
    def send_email(self):
        pass
    
    def validate_email(self):
        pass
    
    def generate_report(self):
        pass
    
    def log_activity(self):
        pass
```

**Solution**: Split responsibilities into separate classes

```python
# ✅ Good: Each class has one responsibility
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save(self, user):
        pass

class EmailService:
    def send(self, user):
        pass

class EmailValidator:
    def validate(self, email):
        pass
```

### 2. Rigid Hierarchy (Violates OCP and LSP)
**Problem**: Classes that are hard to extend without modification

```python
# ❌ Bad: Adding new discount types requires modifying existing code
class DiscountCalculator:
    def calculate(self, discount_type, price):
        if discount_type == "percentage":
            return price * 0.9
        elif discount_type == "fixed":
            return price - 10
        elif discount_type == "buy_one_get_one":
            return price * 0.5
        # Adding new types requires modifying this method
```

**Solution**: Use the Strategy pattern with abstraction

```python
# ✅ Good: New discounts can be added without modifying existing code
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price):
        pass

class PercentageDiscount(DiscountStrategy):
    def apply(self, price):
        return price * 0.9

class BuyOneGetOne(DiscountStrategy):
    def apply(self, price):
        return price * 0.5

class DiscountCalculator:
    def calculate(self, strategy: DiscountStrategy, price):
        return strategy.apply(price)
```

### 3. Complex Interfaces (Violates ISP)
**Problem**: Interfaces that force classes to implement methods they don't need

```python
# ❌ Bad: Worker interface is too complex
class Worker:
    def work(self):
        pass
    
    def eat_lunch(self):
        pass

class Robot(Worker):
    def work(self):
        return "Working..."
    
    def eat_lunch(self):
        raise Exception("Robots don't eat!")  # Forced to implement
```

**Solution**: Segregate interfaces into smaller, focused ones

```python
# ✅ Good: Separated interfaces
class Workable:
    def work(self):
        pass

class Eatable:
    def eat_lunch(self):
        pass

class Human(Workable, Eatable):
    def work(self):
        return "Working..."
    
    def eat_lunch(self):
        return "Eating..."

class Robot(Workable):
    def work(self):
        return "Working..."
```

### 4. Tight Coupling (Violates DIP)
**Problem**: High-level modules depend directly on low-level modules

```python
# ❌ Bad: NotificationService tightly coupled to EmailSender
class EmailSender:
    def send(self, message):
        print(f"Sending email: {message}")

class NotificationService:
    def __init__(self):
        self.sender = EmailSender()  # Direct dependency
    
    def notify(self, message):
        self.sender.send(message)
```

**Solution**: Depend on abstractions through dependency injection

```python
# ✅ Good: Depends on abstraction
from abc import ABC, abstractmethod

class MessageSender(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailSender(MessageSender):
    def send(self, message):
        print(f"Sending email: {message}")

class NotificationService:
    def __init__(self, sender: MessageSender):
        self.sender = sender  # Injected dependency
    
    def notify(self, message):
        self.sender.send(message)
```
