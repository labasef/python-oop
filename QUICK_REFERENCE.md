# Quick Reference Guide

A handy cheat sheet for OOP and SOLID principles in Python.

---

## 🔧 OOP Core Principles Checklist

### Encapsulation
```python
class GoodExample:
    def __init__(self, value):
        self._internal = value  # Protected
        self.__private = value  # Private
    
    @property
    def value(self):
        return self._internal
    
    @value.setter
    def value(self, v):
        if v < 0:
            raise ValueError("Must be positive")
        self._internal = v
```

**Key Points**:
- Use `_attribute` for protected (internal use)
- Use `__attribute` for private (name mangling)
- Use properties for controlled access with validation
- Protect invariants (rules that must always be true)

---

### Inheritance
```python
class Parent:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return "Speaking..."

class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)  # Call parent __init__
        self.age = age
    
    def speak(self):  # Override
        return f"{self.name} says hello!"

# Multiple inheritance
class Mixin:
    def extra_method(self):
        pass

class MultiChild(Parent, Mixin):
    pass
```

**Key Points**:
- Use `super()` to call parent methods
- Override methods by redefining in child class
- Keep hierarchy shallow (max 3 levels)
- Use composition for "has-a" relationships

---

### Polymorphism
```python
class Animal:
    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

# Polymorphic behavior
def make_animal_speak(animal: Animal):
    return animal.speak()

# Works with any Animal subtype
dog = Dog()
cat = Cat()
print(make_animal_speak(dog))   # Woof!
print(make_animal_speak(cat))   # Meow!
```

**Key Points**:
- Different types respond differently to same message
- Enables writing general code that works with subtypes
- Based on shared interface/base class

---

### Abstraction
```python
from abc import ABC, abstractmethod

class Shape(ABC):  # Abstract base class
    @abstractmethod
    def area(self):
        pass  # Must be implemented by subclasses
    
    def describe(self):
        return f"Area: {self.area()}"  # Concrete method

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14 * self.radius ** 2

# Cannot instantiate abstract class
# shape = Shape()  # Error!
circle = Circle(5)
```

**Key Points**:
- Use ABC for abstract base classes
- Use @abstractmethod for methods that must be overridden
- Hides implementation details
- Enforces contract/interface

---

## 💎 SOLID Principles Checklist

### Single Responsibility Principle (SRP)
```python
# ❌ Bad - Too many responsibilities
class User:
    def save_to_db(self): pass
    def send_email(self): pass
    def generate_report(self): pass

# ✅ Good - Single responsibility
class User:
    pass

class UserRepository:
    def save(self, user): pass

class EmailService:
    def send(self, user): pass

class ReportGenerator:
    def generate(self, user): pass
```

**Ask**: "Why would this class change?" If multiple answers → violates SRP

---

### Open/Closed Principle (OCP)
```python
# ❌ Bad - Must modify to add discount types
class PriceCalculator:
    def calculate(self, type, price):
        if type == "percent": return price * 0.9
        elif type == "fixed": return price - 10

# ✅ Good - Open for extension, closed for modification
class Discount:
    def apply(self, price): pass

class PercentDiscount(Discount):
    def apply(self, price): return price * 0.9

class FixedDiscount(Discount):
    def apply(self, price): return price - 10

class PriceCalculator:
    def calculate(self, discount: Discount, price):
        return discount.apply(price)
```

**Ask**: "Can I add new behavior without modifying existing code?"

---

### Liskov Substitution Principle (LSP)
```python
# ❌ Bad - Penguin breaks the Bird contract
class Bird:
    def fly(self): return "Flying"

class Penguin(Bird):
    def fly(self): raise Exception("Can't fly")

# ✅ Good - Respect the contract
class Bird:
    pass

class FlyingBird(Bird):
    def fly(self): return "Flying"

class SwimmingBird(Bird):
    def swim(self): return "Swimming"

class Penguin(SwimmingBird):
    def swim(self): return "Swimming"
```

**Rule**: Subtypes must be substitutable for their base types

---

### Interface Segregation Principle (ISP)
```python
# ❌ Bad - Complex interface
class Machine:
    def print(self): pass
    def scan(self): pass
    def fax(self): pass

class SimplePrinter(Machine):
    def print(self): pass
    def scan(self): raise NotImplementedError  # Forced!
    def fax(self): raise NotImplementedError   # Forced!

# ✅ Good - Segregated interfaces
class Printer:
    def print(self): pass

class Scanner:
    def scan(self): pass

class Fax:
    def fax(self): pass

class MultiFunctionMachine(Printer, Scanner, Fax):
    def print(self): pass
    def scan(self): pass
    def fax(self): pass

class SimplePrinter(Printer):
    def print(self): pass
```

**Ask**: "Does every implementation need all methods?" If no → too complex, split interfaces

---

### Dependency Inversion Principle (DIP)
```python
# ❌ Bad - Depends on concrete class
class EmailService:
    def send(self): pass

class NotificationService:
    def __init__(self):
        self.service = EmailService()  # Direct dependency

# ✅ Good - Depends on abstraction
from abc import ABC, abstractmethod

class MessageService(ABC):
    @abstractmethod
    def send(self): pass

class EmailService(MessageService):
    def send(self): pass

class NotificationService:
    def __init__(self, service: MessageService):
        self.service = service  # Injected, any MessageService works
```

**Rule**: Depend on abstractions, not concrete implementations

---

## 📋 Class Design Checklist

- [ ] Clear, single responsibility
- [ ] Encapsulation: Hide internal state
- [ ] Immutable when possible
- [ ] Use composition over inheritance
- [ ] Follow type hints
- [ ] Proper `__init__`, `__str__`, `__repr__`
- [ ] Document with docstrings
- [ ] Easy to test
- [ ] No circular dependencies
- [ ] Use dataclass for simple data objects

---

## 🎯 Common Patterns at a Glance

| Pattern | Purpose | When to Use |
|---------|---------|-------------|
| **Singleton** | Single instance | Config, logging |
| **Factory** | Create objects | Multiple types |
| **Strategy** | Interchangeable algorithms | Sorting, filters |
| **Decorator** | Add behavior dynamically | Logging, caching |
| **Observer** | Notify multiple objects | Event handling |
| **Template Method** | Define algorithm skeleton | Workflows |
| **Context Manager** | Setup/cleanup | Resources |

---

## 🚫 Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **God Object** | Does too much | Split responsibilities |
| **Deep Hierarchy** | Hard to maintain | Composition over inheritance |
| **Fat Interface** | Forced implementations | Segregate interfaces |
| **Tight Coupling** | Hard to test | Dependency injection |
| **Switch Statements** | Violates OCP | Use polymorphism |
| **Primitive Obsession** | Missing domain logic | Create small objects |

---

## 📝 Essential Python OOP Features

### Property Decorator
```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273:
            raise ValueError("Below absolute zero")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
```

### Class vs Static Methods
```python
class MyClass:
    class_var = "shared"
    
    def instance_method(self):
        """Can access instance and class"""
        return self.class_var
    
    @classmethod
    def class_method(cls):
        """Can only access class"""
        return cls.class_var
    
    @staticmethod
    def static_method():
        """Cannot access instance or class"""
        return "independent"
```

### Dataclass
```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int = 0
    
    def greet(self):
        return f"Hi, I'm {self.name}"

# Automatically creates __init__, __repr__, __eq__, etc.
```

---

## 🧪 Testing Tips

```python
import unittest

class TestMyClass(unittest.TestCase):
    def setUp(self):
        """Called before each test"""
        self.obj = MyClass()
    
    def test_something(self):
        self.assertEqual(self.obj.method(), expected)
    
    def test_exception(self):
        with self.assertRaises(ValueError):
            self.obj.invalid_method()
    
    def tearDown(self):
        """Called after each test"""
        pass
```

---

## 💡 Pro Tips

1. **Use type hints**: Helps catch errors early
   ```python
   def process(items: list[str]) -> dict[str, int]:
       pass
   ```

2. **Use `__all__`**: Define public API
   ```python
   __all__ = ['PublicClass', 'public_function']
   ```

3. **Use descriptive names**: Class names are nouns, methods are verbs
   ```python
   class UserRepository:  # Noun
       def find_by_id(self):  # Verb
           pass
   ```

4. **Use composition**: More flexible than inheritance
   ```python
   class Car:
       def __init__(self, engine, wheels):
           self.engine = engine
           self.wheels = wheels
   ```

5. **Avoid mutable defaults**: Use None and create inside method
   ```python
   def __init__(self, items=None):
       self.items = items or []
   ```

---

## Quick Decision Trees

### Should I use Inheritance?
```
Is it truly "IS-A" relationship?
├─ YES → Consider inheritance
├─ NO → Use composition

Does it create deep hierarchy (>3 levels)?
├─ YES → Flatten or use composition
├─ NO → OK to use inheritance
```

### Should I use Abstraction?
```
Do I have multiple implementations?
├─ YES → Use abstract base class
├─ NO → Keep it simple

Will there be new implementations later?
├─ YES → Design abstraction early
├─ NO → Use YAGNI principle
```

---

**Remember**: Write code for humans first, computers second. Clear, maintainable code is better than clever code.


