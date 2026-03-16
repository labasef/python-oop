class StateFul:
    # Class attributes are shared by all instances of the class
    # They can be accessed using the class name or the instance
    # Within the class, they can be accessed using the cls keyword
    a = "Class attribute"

    def __init__(self):
        # Instance attributes are unique to each instance of the class
        # They can be accessed using the instance
        # Within the class, they can be accessed using the self keyword
        # They can be defined in the __init__ method or any other method
        self.a = "Instance attribute"

    # Static methods don't have access to the class or instance methods and attributes
    # They are just like regular functions, but they belong to the class
    @staticmethod
    def foo(a: str):
        return "FOO " + a.upper()

    # Class methods have access to the class but not the instance methods and attributes
    @classmethod
    def bar(cls):
        return "BAR " + cls.foo(cls.a)

    # Instance methods have access to the instance and the class methods and attributes
    # They can change the state of the instance
    def boo(self):
        return "BOO " + self.a.upper()


print(StateFul.foo("hello"))  # Output: FOO HELLO
print(StateFul.bar())  # Output: BAR FOO CLASS ATTRIBUTE
obj = StateFul()
print(obj.boo())  # Output: BOO INSTANCE ATTRIBUTE
print(obj.bar())  # Output: BAR FOO CLASS ATTRIBUTE

class StateLess:
    # Static methods don't have access to the class or instance
    @staticmethod
    def foo(a: str):
        return "FOO " + a.upper()

    # Class methods have access to the class but not the instance
    @classmethod
    def bar(cls, a: str):
        return "BAR " + cls.foo(a)


# You don't need to instantiate the class to use the methods
print(StateLess.foo("hello"))  # Output: FOO HELLO
print(StateLess.bar("hello"))  # Output: BAR FOO HELLO




class Bar:
    class_state = 1

    @classmethod
    def class_up(cls):
        cls.class_state += 1
        return cls

    @classmethod
    def class_down(cls):
        cls.class_state -= 1
        return cls

    def __init__(self):
        self.state = 1

    def up(self):
        self.state += 1
        return self

    def down(self):
        self.state -= 1
        return self

print(Bar.class_state)  # Output: 1

# instantiating the class
bar = Bar()
print('class state of instance:', bar.class_state)  # Output: 1
print('state of instance', bar.state)  # Output: 1
print('state of instance', bar.up().state)  # Output: 2

# incrementing the class state
Bar.class_up()
print('class state of instance:', bar.class_state)  # Output: 2

print(Bar.__dict__)
print(bar.__dict__)

# Changing state at class and instance level
class FooImmutable:
    # Immutable state
    state = 1

    # Class methods have access to the class but not the instance
    # They can change the state of the class
    @classmethod
    def up(cls):
        cls.state += 1
        return cls

    # Instance methods have access to the instance and the class
    # They can change the state of the instance
    def down(self):
        # a new state reference in the instance namespace is created
        # the state reference in the class namespace is not modified
        self.state -= 1
        return self


class FooMutable:
    # Mutable state
    state = []

    # Class methods have access to the class but not the instance
    # They can change the state of the class
    @classmethod
    def up(cls):
        cls.state.append(1)
        return cls

    # Instance methods have access to the instance and the class
    # They can change the state of the instance
    def down(self):
        # the state reference iis found in the class namespace
        # the state reference in the class namespace is modified
        self.state.append(1)
        return self

# changing state at class level
print(FooImmutable.state)  # Output: 1
print(FooImmutable.up().up().state)  # Output: 3

# changing state at instance level
foo = FooImmutable()
# instance state is inherited from the class state
print(foo.state)  # Output: 3
print(foo.down().state)  # Output: 2
# instance state is independent of the class state
print(FooImmutable.state)  # Output: 3

bar = FooMutable()
print(bar.state)  # Output: 3
print(bar.down().down().state)  # Output: 1
print(FooImmutable.up().state)  # Output: 4
print(bar.state)  # Output: 1

print(FooMutable.__dict__)
print(bar.__dict__)

