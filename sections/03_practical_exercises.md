# Practical Exercises

## Purpose

These exercises help reinforce your understanding of OOP and SOLID principles by applying them to real-world scenarios. Start with simpler exercises and gradually work toward more complex ones.

- Use type hints for clarity
- Create separate modules for different classes
- Use `__all__` to define public API
- Document with docstrings
- Follow PEP 8 style guide

---

## Exercise 1: Bank Account System (Encapsulation & Abstraction)

**Difficulty**: ⭐ Easy

**Objective**: Implement a secure bank account system using encapsulation.

**Requirements**:
- Create a `BankAccount` class that encapsulates balance (private attribute)
- Only allow valid operations: deposit, withdraw
- Implement transaction history tracking
- Prevent invalid operations (negative balance, invalid amounts)
- Use properties for controlled access to balance

**Example Structure**:
```python
class BankAccount:
    def __init__(self, account_number: str, initial_balance: float = 0):
        self.__account_number = account_number
        self.__balance = initial_balance
        self.__transaction_history = []
    
    @property
    def balance(self):
        return self.__balance
    
    def deposit(self, amount: float) -> bool:
        # Implementation
        pass
    
    def withdraw(self, amount: float) -> bool:
        # Implementation
        pass
    
    def get_transaction_history(self):
        # Implementation
        pass
```

**Bonus Challenges**:
- Add interest calculation
- Implement different account types (Savings, Checking)
- Add overdraft protection

---

## Exercise 2: Shape Calculator (Inheritance & Polymorphism)

**Difficulty**: ⭐⭐ Medium

**Objective**: Create a shape system that demonstrates inheritance and polymorphism.

**Requirements**:
- Create an abstract `Shape` class with abstract method `area()`
- Implement concrete shapes: `Circle`, `Rectangle`, `Triangle`
- Create a `ShapeCalculator` that works with any shape (polymorphism)
- Implement proper calculation logic for each shape

**Example Structure**:
```python
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass

# Implement Circle, Rectangle, Triangle...

class ShapeCalculator:
    def calculate_total_area(self, shapes: list) -> float:
        return sum(shape.area() for shape in shapes)
```

**Bonus Challenges**:
- Add 3D shapes (Sphere, Cube)
- Implement comparison operators
- Create a shape registry system

---

## Exercise 3: E-commerce Discount System (SOLID Principles)

**Difficulty**: ⭐⭐⭐ Medium-Hard

**Objective**: Design a flexible discount system following SOLID principles.

**Requirements**:
- Create an abstract `DiscountStrategy` (OCP)
- Implement different discount types: Percentage, Fixed, BuyOneGetOne
- Each discount is a separate class (SRP)
- `Order` class should accept any discount strategy (DIP)
- Prices should never become negative

**Example Structure**:
```python
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, original_price: float) -> float:
        pass

class Order:
    def __init__(self, items: list, discount_strategy: DiscountStrategy = None):
        self.items = items
        self.discount_strategy = discount_strategy
    
    def calculate_total(self) -> float:
        # Implementation
        pass
```

**Bonus Challenges**:
- Implement combinable discounts
- Add discount validation
- Create a loyalty point system
- Add tax calculations

---

## Exercise 4: Email Notification System (Dependency Injection & DIP)

**Difficulty**: ⭐⭐⭐ Medium-Hard

**Objective**: Build a flexible notification system using dependency injection.

**Requirements**:
- Create abstract `NotificationSender` interface
- Implement multiple senders: Email, SMS, Slack
- `NotificationService` should accept any sender via DI
- Easy to add new notification types without modifying existing code
- Handle failures gracefully

**Example Structure**:
```python
from abc import ABC, abstractmethod

class NotificationSender(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass

class NotificationService:
    def __init__(self, sender: NotificationSender):
        self.sender = sender
    
    def notify_user(self, user_id: str, message: str) -> bool:
        # Implementation
        pass
```

**Bonus Challenges**:
- Implement retry logic
- Add message templates
- Create a multi-sender notification system
- Add logging and auditing

---

## Exercise 5: Library Management System (All Principles)

**Difficulty**: ⭐⭐⭐⭐ Hard

**Objective**: Build a comprehensive library system using all OOP and SOLID principles.

**Requirements**:
- `Book` class with encapsulated attributes
- `Member` class managing book borrowing
- `Library` class managing the collection
- Implement lending rules (max books, due dates)
- Create abstract `Library` interface for extensibility
- Each class has single responsibility
- Use dependency injection for repositories

**Key Classes**:
```python
class Book:
    # Encapsulate book data
    pass

class Member:
    # Manage member information
    pass

class LibraryRepository(ABC):
    # Abstract repository pattern
    pass

class LibraryService:
    # Business logic
    def __init__(self, repository: LibraryRepository):
        self.repository = repository
```

**Bonus Challenges**:
- Add book categories and searching
- Implement fine calculation system
- Add reservation system
- Create reporting functionality
- Implement user roles (Admin, Librarian, Member)

---

## Exercise 6: Design Pattern Implementation (Observer Pattern)

**Difficulty**: ⭐⭐⭐ Medium-Hard

**Objective**: Implement the Observer pattern in a practical scenario.

**Requirements**:
- Create a `Subject` that notifies multiple `Observers`
- Real-world example: Stock market price changes
- Observers automatically react to subject changes
- Easy to add/remove observers dynamically

**Example Structure**:
```python
class StockPrice:
    """Subject - notifies observers of price changes"""
    pass

class TradingBot(Observer):
    """Observer - reacts to price changes"""
    pass

class Investor(Observer):
    """Observer - gets notified of price changes"""
    pass
```

**Bonus Challenges**:
- Implement multiple observer types
- Add filtering by price threshold
- Create historical data tracking
- Implement unsubscribe functionality

---

## Self-Assessment Checklist

After completing these exercises, verify that your code:

- **Encapsulation**: Private attributes with controlled access
- **Inheritance**: Proper use of base classes and super()
- **Polymorphism**: Different objects work through same interface
- **Abstraction**: ABC and abstractmethod used appropriately
- **SRP**: Each class has one reason to change
- **OCP**: Open for extension, closed for modification
- **LSP**: Substitutable subtypes
- **ISP**: Focused, segregated interfaces
- **DIP**: Depends on abstractions, not concrete classes
- **Testing**: Code is easily testable
- **Documentation**: Clear docstrings explaining purpose

---

## Tips for Success

1. **Start Simple**: Begin with Exercise 1 and 2 before moving to complex ones
2. **Refactor**: Write a basic solution first, then refactor to apply SOLID principles
3. **Test**: Write unit tests to verify your implementation
4. **Review**: Check against the checklist above
5. **Share**: Get code reviews from peers to learn different approaches

---

## Solutions

When you're ready to compare your work, the full solutions are available here:

👉 **[View Solutions](./03_practical_exercises_solutions.md)**

Each solution includes a short explanation of which OOP and SOLID principles are demonstrated.


