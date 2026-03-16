"""
Dunder Methods: Object Construction & Destruction
__new__, __init__, __del__

- __new__  : Creates the instance (before __init__)
- __init__ : Initialises the instance (called after __new__)
- __del__  : Called just before the instance is destroyed (garbage collected)

Medical theme: Hospital patient registration system.
"""


class Patient:
    """
    Demonstrates __new__ and __init__.

    __new__ is responsible for creating a blank instance of the class.
    __init__ is responsible for setting its initial state.
    In everyday code you only override __init__; __new__ is shown here
    purely for illustration.
    """

    # Class-level counter to auto-generate patient IDs
    _id_counter = 1000

    def __new__(cls, *args, **kwargs):
        """
        __new__ is called FIRST.
        It creates and returns a new (uninitialised) instance of the class.
        """
        instance = super().__new__(cls)
        # Assign a unique ID before __init__ runs
        cls._id_counter += 1
        instance.patient_id = f"P{cls._id_counter}"
        print(f"[__new__]  Allocating memory for new Patient (id={instance.patient_id})")
        return instance

    def __init__(self, name: str, age: int, condition: str):
        """
        __init__ is called SECOND, on the instance __new__ returned.
        It populates the instance with data.
        """
        print(f"[__init__] Initialising Patient {self.patient_id}: {name}")
        self.name = name
        self.age = age
        self.condition = condition
        self.is_admitted = False

    def admit(self):
        self.is_admitted = True
        print(f"  {self.name} admitted to hospital.")

    def discharge(self):
        self.is_admitted = False
        print(f"  {self.name} discharged from hospital.")

    def __del__(self):
        """
        __del__ is called just before the object is garbage-collected.
        Use sparingly — don't rely on it for critical cleanup (use context
        managers for that).  Here it simply logs when a record is removed.
        """
        print(f"[__del__]  Patient record {self.patient_id} ({self.name}) removed from memory.")


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Construction Dunders: Patient Registration ===\n")

    print("--- Creating patients ---")
    alice = Patient("Alice Smith",  34, "Hypertension")
    bob   = Patient("Bob Johnson",  52, "Diabetes Type 2")
    print()

    print("--- Using patients ---")
    alice.admit()
    bob.admit()
    alice.discharge()
    print()

    print("--- Deleting a record (triggers __del__) ---")
    del alice
    print()

    print("--- End of script (remaining objects cleaned up) ---")
    # bob.__del__ fires here when the interpreter exits

