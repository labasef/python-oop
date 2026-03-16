# Practical Exercises — Solutions

> **Note**: Try to complete each exercise yourself before reading the solutions!

---

## Solution 1: Bank Account System

```python
from datetime import datetime


class BankAccount:
    def __init__(self, account_number: str, initial_balance: float = 0):
        self.__account_number = account_number
        self.__balance = initial_balance
        self.__transaction_history = []
        if initial_balance > 0:
            self.__record_transaction("initial deposit", initial_balance)

    @property
    def account_number(self):
        return self.__account_number

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__balance += amount
        self.__record_transaction("deposit", amount)
        return True

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        self.__record_transaction("withdrawal", -amount)
        return True

    def get_transaction_history(self) -> list:
        return list(self.__transaction_history)

    def __record_transaction(self, transaction_type: str, amount: float):
        self.__transaction_history.append({
            "type": transaction_type,
            "amount": amount,
            "balance": self.__balance,
            "timestamp": datetime.now().isoformat()
        })

    def __str__(self):
        return f"BankAccount({self.__account_number}, balance={self.__balance:.2f})"


# Bonus: Different account types using inheritance
class SavingsAccount(BankAccount):
    def __init__(self, account_number: str, initial_balance: float = 0, interest_rate: float = 0.05):
        super().__init__(account_number, initial_balance)
        self.__interest_rate = interest_rate

    def apply_interest(self) -> float:
        interest = self.balance * self.__interest_rate
        self.deposit(interest)
        return interest


class CheckingAccount(BankAccount):
    def __init__(self, account_number: str, initial_balance: float = 0, overdraft_limit: float = 100):
        super().__init__(account_number, initial_balance)
        self.__overdraft_limit = overdraft_limit

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance + self.__overdraft_limit:
            raise ValueError("Exceeds overdraft limit")
        if amount > self.balance:
            print(f"Warning: overdraft of {amount - self.balance:.2f}")
        return super().withdraw(min(amount, self.balance)) or True


# Usage
account = SavingsAccount("SA001", 1000, interest_rate=0.05)
account.deposit(500)
account.withdraw(200)
interest = account.apply_interest()
print(f"Balance: {account.balance:.2f}")   # 1342.50
print(f"Interest earned: {interest:.2f}")  # 63.75
for tx in account.get_transaction_history():
    print(tx)
```

**Principles applied**:
- **Encapsulation**: `__balance` and `__transaction_history` are private; access is controlled via properties and methods
- **Inheritance**: `SavingsAccount` and `CheckingAccount` extend `BankAccount` via `super()`
- **Abstraction**: Users interact with `deposit`/`withdraw` without knowing the internals

---

## Solution 2: Shape Calculator

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

    def __str__(self):
        return f"{self.__class__.__name__}(area={self.area():.2f}, perimeter={self.perimeter():.2f})"

    def __lt__(self, other: "Shape") -> bool:
        return self.area() < other.area()

    def __eq__(self, other: "Shape") -> bool:
        return self.area() == other.area()


class Circle(Shape):
    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("Radius must be positive")
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        if width <= 0 or height <= 0:
            raise ValueError("Dimensions must be positive")
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Sides must be positive")
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Invalid triangle sides")
        self.a, self.b, self.c = a, b, c

    def area(self) -> float:
        s = self.perimeter() / 2  # Heron's formula
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c


# Bonus: 3D shape
class Sphere(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:  # Surface area
        return 4 * math.pi * self.radius ** 2

    def perimeter(self) -> float:  # Great-circle circumference
        return 2 * math.pi * self.radius

    def volume(self) -> float:
        return (4 / 3) * math.pi * self.radius ** 3


class ShapeCalculator:
    def calculate_total_area(self, shapes: list[Shape]) -> float:
        return sum(shape.area() for shape in shapes)

    def calculate_total_perimeter(self, shapes: list[Shape]) -> float:
        return sum(shape.perimeter() for shape in shapes)

    def find_largest(self, shapes: list[Shape]) -> Shape:
        return max(shapes, key=lambda s: s.area())

    def find_smallest(self, shapes: list[Shape]) -> Shape:
        return min(shapes, key=lambda s: s.area())

    def sort_by_area(self, shapes: list[Shape]) -> list[Shape]:
        return sorted(shapes, key=lambda s: s.area())


# Usage
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5), Sphere(3)]
calc = ShapeCalculator()

print(f"Total area:  {calc.calculate_total_area(shapes):.2f}")
print(f"Largest:     {calc.find_largest(shapes)}")
print(f"Smallest:    {calc.find_smallest(shapes)}")
for shape in calc.sort_by_area(shapes):
    print(shape)
```

**Principles applied**:
- **Abstraction**: `Shape` is an ABC with abstract `area()` and `perimeter()`
- **Inheritance**: All shapes extend `Shape`
- **Polymorphism**: `ShapeCalculator` works with any `Shape` subtype without knowing its concrete class

---

## Solution 3: E-commerce Discount System

```python
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, original_price: float) -> float:
        pass

    def __repr__(self):
        return self.__class__.__name__


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        if not 0 < percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        self.percentage = percentage

    def calculate(self, original_price: float) -> float:
        return original_price * (1 - self.percentage / 100)


class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        if amount <= 0:
            raise ValueError("Discount amount must be positive")
        self.amount = amount

    def calculate(self, original_price: float) -> float:
        return max(0.0, original_price - self.amount)  # Never goes negative


class BuyOneGetOne(DiscountStrategy):
    """50% off — equivalent to buy one, get one free."""
    def calculate(self, original_price: float) -> float:
        return original_price * 0.5


# Bonus: chain multiple strategies
class CombinedDiscount(DiscountStrategy):
    def __init__(self, *strategies: DiscountStrategy):
        self.strategies = strategies

    def calculate(self, original_price: float) -> float:
        price = original_price
        for strategy in self.strategies:
            price = strategy.calculate(price)
        return price


class OrderItem:
    def __init__(self, name: str, price: float, quantity: int = 1):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        self.name = name
        self.price = price
        self.quantity = quantity

    def subtotal(self) -> float:
        return self.price * self.quantity


class Order:
    TAX_RATE = 0.1  # 10%

    def __init__(self, items: list[OrderItem], discount_strategy: DiscountStrategy = None):
        self.items = items
        self.discount_strategy = discount_strategy

    def subtotal(self) -> float:
        return sum(item.subtotal() for item in self.items)

    def discount_amount(self) -> float:
        if not self.discount_strategy:
            return 0.0
        return self.subtotal() - self.discount_strategy.calculate(self.subtotal())

    def discounted_subtotal(self) -> float:
        if not self.discount_strategy:
            return self.subtotal()
        return self.discount_strategy.calculate(self.subtotal())

    def tax(self) -> float:
        return self.discounted_subtotal() * self.TAX_RATE

    def calculate_total(self) -> float:
        return self.discounted_subtotal() + self.tax()

    def receipt(self) -> str:
        lines = ["=== Order Receipt ==="]
        for item in self.items:
            lines.append(f"  {item.name} x{item.quantity}: £{item.subtotal():.2f}")
        lines.append(f"Subtotal:  £{self.subtotal():.2f}")
        lines.append(f"Discount:  -£{self.discount_amount():.2f} ({self.discount_strategy or 'None'})")
        lines.append(f"Tax (10%): £{self.tax():.2f}")
        lines.append(f"Total:     £{self.calculate_total():.2f}")
        return "\n".join(lines)


# Usage
items = [
    OrderItem("Laptop", 999.99),
    OrderItem("Mouse", 29.99, quantity=2),
]

order = Order(items, PercentageDiscount(10))
print(order.receipt())

# Bonus: stacked discounts
combo = CombinedDiscount(PercentageDiscount(10), FixedDiscount(50))
order2 = Order(items, combo)
print(order2.receipt())
```

**Principles applied**:
- **SRP**: Each discount type is its own class; `Order` only handles totalling
- **OCP**: New discount types extend `DiscountStrategy` without touching `Order`
- **DIP**: `Order` depends on the abstract `DiscountStrategy`, not a concrete class

---

## Solution 4: Notification System

```python
from abc import ABC, abstractmethod
import time


class NotificationSender(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass


class EmailSender(NotificationSender):
    def send(self, recipient: str, message: str) -> bool:
        print(f"[EMAIL] To: {recipient} | Message: {message}")
        return True


class SMSSender(NotificationSender):
    def send(self, recipient: str, message: str) -> bool:
        print(f"[SMS] To: {recipient} | Message: {message}")
        return True


class SlackSender(NotificationSender):
    def __init__(self, channel: str):
        self.channel = channel

    def send(self, recipient: str, message: str) -> bool:
        print(f"[SLACK #{self.channel}] To: {recipient} | Message: {message}")
        return True


# Bonus: broadcast across multiple channels
class MultiSender(NotificationSender):
    def __init__(self, *senders: NotificationSender):
        self.senders = senders

    def send(self, recipient: str, message: str) -> bool:
        return all(sender.send(recipient, message) for sender in self.senders)


class NotificationService:
    def __init__(self, sender: NotificationSender, max_retries: int = 3):
        if not isinstance(sender, NotificationSender):
            raise TypeError("sender must be a NotificationSender")
        self.sender = sender
        self.max_retries = max_retries
        self._audit_log: list[dict] = []

    def notify_user(self, user_id: str, message: str) -> bool:
        for attempt in range(1, self.max_retries + 1):
            try:
                success = self.sender.send(user_id, message)
                self._log(user_id, message, success)
                return success
            except Exception as e:
                print(f"Attempt {attempt} failed: {e}")
                if attempt < self.max_retries:
                    time.sleep(0.1)
        self._log(user_id, message, False)
        return False

    def _log(self, user_id: str, message: str, success: bool):
        self._audit_log.append({
            "user_id": user_id,
            "message": message,
            "success": success,
            "timestamp": time.time()
        })

    def get_audit_log(self) -> list[dict]:
        return list(self._audit_log)


# Usage
email_service = NotificationService(EmailSender())
email_service.notify_user("user@example.com", "Your order has shipped!")

sms_service = NotificationService(SMSSender())
sms_service.notify_user("+447700900000", "Your OTP is 123456")

# Multi-channel
multi = NotificationService(MultiSender(EmailSender(), SMSSender()))
multi.notify_user("alice@example.com", "System maintenance tonight at 10pm")
```

**Principles applied**:
- **DIP**: `NotificationService` depends on the abstract `NotificationSender`
- **OCP**: New channel types (e.g. `PushNotificationSender`) need no changes to `NotificationService`
- **ISP**: `NotificationSender` exposes only the single method each sender needs

---

## Solution 5: Library Management System

```python
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum


class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"


class Book:
    def __init__(self, isbn: str, title: str, author: str, category: str = "General"):
        self.__isbn = isbn
        self.title = title
        self.author = author
        self.category = category
        self.__status = BookStatus.AVAILABLE

    @property
    def isbn(self):
        return self.__isbn

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, new_status: BookStatus):
        if not isinstance(new_status, BookStatus):
            raise ValueError("Invalid book status")
        self.__status = new_status

    def is_available(self) -> bool:
        return self.__status == BookStatus.AVAILABLE

    def __str__(self):
        return f'"{self.title}" by {self.author} [{self.__status.value}]'


class Loan:
    LOAN_PERIOD_DAYS = 14
    FINE_PER_DAY = 0.50

    def __init__(self, book: Book, member_id: str):
        self.book = book
        self.member_id = member_id
        self.borrowed_at = datetime.now()
        self.due_date = self.borrowed_at + timedelta(days=self.LOAN_PERIOD_DAYS)
        self.returned_at = None

    def is_overdue(self) -> bool:
        end = self.returned_at or datetime.now()
        return end > self.due_date

    def fine(self) -> float:
        if not self.is_overdue():
            return 0.0
        end = self.returned_at or datetime.now()
        overdue_days = (end - self.due_date).days
        return overdue_days * self.FINE_PER_DAY

    def return_book(self):
        self.returned_at = datetime.now()
        self.book.status = BookStatus.AVAILABLE


class Member:
    MAX_BOOKS = 5

    def __init__(self, member_id: str, name: str):
        self.__member_id = member_id
        self.name = name
        self.__loans: list[Loan] = []

    @property
    def member_id(self):
        return self.__member_id

    @property
    def active_loans(self) -> list[Loan]:
        return [loan for loan in self.__loans if loan.returned_at is None]

    def can_borrow(self) -> bool:
        return len(self.active_loans) < self.MAX_BOOKS

    def add_loan(self, loan: Loan):
        self.__loans.append(loan)

    def total_fines(self) -> float:
        return sum(loan.fine() for loan in self.__loans)

    def loan_history(self) -> list[Loan]:
        return list(self.__loans)


class LibraryRepository(ABC):
    @abstractmethod
    def add_book(self, book: Book): pass

    @abstractmethod
    def find_book(self, isbn: str) -> Book | None: pass

    @abstractmethod
    def search_books(self, query: str) -> list[Book]: pass

    @abstractmethod
    def add_member(self, member: Member): pass

    @abstractmethod
    def find_member(self, member_id: str) -> Member | None: pass


class InMemoryLibraryRepository(LibraryRepository):
    def __init__(self):
        self.__books: dict[str, Book] = {}
        self.__members: dict[str, Member] = {}

    def add_book(self, book: Book):
        self.__books[book.isbn] = book

    def find_book(self, isbn: str) -> Book | None:
        return self.__books.get(isbn)

    def search_books(self, query: str) -> list[Book]:
        query = query.lower()
        return [
            book for book in self.__books.values()
            if query in book.title.lower()
            or query in book.author.lower()
            or query in book.category.lower()
        ]

    def add_member(self, member: Member):
        self.__members[member.member_id] = member

    def find_member(self, member_id: str) -> Member | None:
        return self.__members.get(member_id)


class LibraryService:
    def __init__(self, repository: LibraryRepository):
        self.repository = repository

    def borrow_book(self, member_id: str, isbn: str) -> Loan:
        member = self.repository.find_member(member_id)
        if not member:
            raise ValueError(f"Member {member_id} not found")
        book = self.repository.find_book(isbn)
        if not book:
            raise ValueError(f"Book {isbn} not found")
        if not book.is_available():
            raise ValueError(f'"{book.title}" is not currently available')
        if not member.can_borrow():
            raise ValueError(f"{member.name} has reached the borrowing limit")

        loan = Loan(book, member_id)
        book.status = BookStatus.BORROWED
        member.add_loan(loan)
        print(f'{member.name} borrowed "{book.title}"')
        return loan

    def return_book(self, member_id: str, isbn: str) -> float:
        member = self.repository.find_member(member_id)
        if not member:
            raise ValueError(f"Member {member_id} not found")
        loan = next(
            (l for l in member.active_loans if l.book.isbn == isbn), None
        )
        if not loan:
            raise ValueError(f"No active loan found for book {isbn}")

        loan.return_book()
        fine = loan.fine()
        if fine > 0:
            print(f'"{loan.book.title}" returned. Fine: £{fine:.2f}')
        else:
            print(f'"{loan.book.title}" returned on time.')
        return fine


# Usage
repo = InMemoryLibraryRepository()
service = LibraryService(repo)

repo.add_book(Book("978-0-06-112008-4", "To Kill a Mockingbird", "Harper Lee", "Fiction"))
repo.add_book(Book("978-0-7432-7356-5", "1984", "George Orwell", "Dystopian"))
repo.add_member(Member("M001", "Alice"))
repo.add_member(Member("M002", "Bob"))

service.borrow_book("M001", "978-0-06-112008-4")

results = repo.search_books("orwell")
for book in results:
    print(book)

service.return_book("M001", "978-0-06-112008-4")
```

**Principles applied**:
- **Encapsulation**: `Book.__isbn`, `Member.__loans` are private with controlled access
- **SRP**: `Book`, `Loan`, `Member`, `LibraryRepository`, and `LibraryService` each have one responsibility
- **OCP / DIP**: `LibraryService` depends on the abstract `LibraryRepository` — swap in a database-backed repo with zero changes to `LibraryService`

---

## Solution 6: Observer Pattern (Stock Market)

```python
from abc import ABC, abstractmethod
from datetime import datetime


class Observer(ABC):
    @abstractmethod
    def update(self, stock_name: str, price: float, change: float):
        pass


class StockPrice:
    """Subject — notifies all observers when its price changes."""

    def __init__(self, name: str, initial_price: float):
        self.name = name
        self.__price = initial_price
        self.__observers: list[Observer] = []
        self.__history: list[dict] = [
            {"price": initial_price, "timestamp": datetime.now()}
        ]

    @property
    def price(self):
        return self.__price

    def attach(self, observer: Observer):
        if observer not in self.__observers:
            self.__observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def set_price(self, new_price: float):
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        change = new_price - self.__price
        self.__price = new_price
        self.__history.append({"price": new_price, "timestamp": datetime.now()})
        self.__notify_observers(change)

    def get_history(self) -> list[dict]:
        return list(self.__history)

    def __notify_observers(self, change: float):
        for observer in self.__observers:
            observer.update(self.name, self.__price, change)


class Investor(Observer):
    """Logs every price movement."""

    def __init__(self, name: str):
        self.name = name

    def update(self, stock_name: str, price: float, change: float):
        direction = "📈" if change >= 0 else "📉"
        print(f"[Investor {self.name}] {stock_name}: £{price:.2f} ({change:+.2f}) {direction}")


class TradingBot(Observer):
    """Automatically buys or sells when price crosses a threshold."""

    def __init__(self, name: str, buy_below: float, sell_above: float):
        self.name = name
        self.buy_below = buy_below
        self.sell_above = sell_above

    def update(self, stock_name: str, price: float, change: float):
        if price < self.buy_below:
            print(f"[Bot {self.name}] AUTO-BUY {stock_name} at £{price:.2f}")
        elif price > self.sell_above:
            print(f"[Bot {self.name}] AUTO-SELL {stock_name} at £{price:.2f}")


class AlertService(Observer):
    """Fires an alert when the price moves by more than a set percentage."""

    def __init__(self, threshold_pct: float = 5.0):
        self.threshold_pct = threshold_pct

    def update(self, stock_name: str, price: float, change: float):
        previous = price - change
        if previous != 0:
            change_pct = abs(change / previous) * 100
            if change_pct >= self.threshold_pct:
                direction = "dropped" if change < 0 else "jumped"
                print(f"[ALERT] {stock_name} {direction} by {change_pct:.1f}%!")


# Usage
stock = StockPrice("ACME Corp", 100.0)

alice = Investor("Alice")
bot   = TradingBot("AutoTrader", buy_below=90.0, sell_above=120.0)
alerts = AlertService(threshold_pct=5.0)

stock.attach(alice)
stock.attach(bot)
stock.attach(alerts)

print("--- Price updates ---")
stock.set_price(105.0)
stock.set_price(88.0)    # Bot auto-buys; alert fires
stock.set_price(125.0)   # Bot auto-sells; alert fires

print("\n--- Bob joins, Alice leaves ---")
bob = Investor("Bob")
stock.attach(bob)
stock.detach(alice)
stock.set_price(115.0)

print(f"\nPrice history for {stock.name}:")
for entry in stock.get_history():
    print(f"  £{entry['price']:.2f} at {entry['timestamp'].strftime('%H:%M:%S')}")
```

**Principles applied**:
- **Encapsulation**: `StockPrice.__price` and `__observers` are private
- **OCP**: New observer types (e.g. `EmailAlert`) can be added without touching `StockPrice`
- **DIP**: `StockPrice` depends on the abstract `Observer`, not on any concrete class
- **SRP**: Each observer has a single, focused reaction to a price change

