"""
Dunder Methods: Container & Sequence Protocol
__len__, __getitem__, __setitem__, __delitem__, __contains__,
__iter__, __next__, __reversed__

- __len__      : len(obj)
- __getitem__  : obj[key]
- __setitem__  : obj[key] = value
- __delitem__  : del obj[key]
- __contains__ : item in obj
- __iter__     : for item in obj  (returns an iterator)
- __next__     : advances the iterator
- __reversed__ : reversed(obj)

Medical theme: A ward's patient list managed as a custom container.
"""


class WardIterator:
    """
    Separate iterator object for Ward.

    It is best practice to keep the container (__iter__ returns self
    only if the container IS the iterator) and the iterator in separate
    classes so multiple independent iterations can run at the same time.
    """

    def __init__(self, patients: list):
        self._patients = patients
        self._index = 0

    def __iter__(self):
        """An iterator is itself iterable."""
        return self

    def __next__(self):
        """Return the next patient; raise StopIteration when exhausted."""
        if self._index >= len(self._patients):
            raise StopIteration
        patient = self._patients[self._index]
        self._index += 1
        return patient


class Ward:
    """
    A hospital ward that manages a list of patients.

    Implements the full container protocol so the ward can be used
    naturally with len(), [], del, in, for, reversed(), etc.
    """

    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity
        self._patients: list[str] = []

    # ------------------------------------------------------------------
    # __len__ — supports len(ward)
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self._patients)

    # ------------------------------------------------------------------
    # __getitem__ — supports ward[0], ward[-1], ward[1:3]
    # ------------------------------------------------------------------
    def __getitem__(self, index):
        return self._patients[index]

    # ------------------------------------------------------------------
    # __setitem__ — supports ward[0] = "New Patient"
    # ------------------------------------------------------------------
    def __setitem__(self, index: int, patient_name: str):
        self._patients[index] = patient_name
        print(f"  Bed {index} reassigned to {patient_name}")

    # ------------------------------------------------------------------
    # __delitem__ — supports del ward[0]
    # ------------------------------------------------------------------
    def __delitem__(self, index: int):
        removed = self._patients.pop(index)
        print(f"  {removed} discharged from bed {index}")

    # ------------------------------------------------------------------
    # __contains__ — supports "Alice" in ward
    # ------------------------------------------------------------------
    def __contains__(self, patient_name: str) -> bool:
        return patient_name in self._patients

    # ------------------------------------------------------------------
    # __iter__ — supports: for patient in ward
    # Returns a fresh iterator each time so nested loops work correctly.
    # ------------------------------------------------------------------
    def __iter__(self) -> WardIterator:
        return WardIterator(list(self._patients))

    # ------------------------------------------------------------------
    # __reversed__ — supports reversed(ward)
    # ------------------------------------------------------------------
    def __reversed__(self):
        return WardIterator(list(reversed(self._patients)))

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------
    def admit(self, patient_name: str):
        if len(self) >= self.capacity:
            raise OverflowError(f"{self.name} is at full capacity ({self.capacity})")
        self._patients.append(patient_name)
        print(f"  Admitted: {patient_name} → bed {len(self) - 1}")

    def __repr__(self) -> str:
        return f"Ward({self.name!r}, {len(self)}/{self.capacity} beds)"

    def __str__(self) -> str:
        beds = "\n".join(
            f"  Bed {i}: {name}" for i, name in enumerate(self._patients)
        ) or "  (empty)"
        return f"Ward: {self.name}\n{beds}"


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Container Dunders: Hospital Ward ===\n")

    ward = Ward("Cardiology", capacity=5)

    print("--- Admitting patients ---")
    ward.admit("Alice Smith")
    ward.admit("Bob Johnson")
    ward.admit("Carol White")
    ward.admit("David Brown")
    print()

    # __len__
    print(f"__len__      len(ward)          = {len(ward)}")
    print()

    # __getitem__
    print(f"__getitem__  ward[0]            = {ward[0]}")
    print(f"__getitem__  ward[-1]           = {ward[-1]}")
    print(f"__getitem__  ward[1:3]          = {ward[1:3]}")
    print()

    # __contains__
    print(f"__contains__ 'Alice Smith' in ward  = {'Alice Smith' in ward}")
    print(f"__contains__ 'John Doe'    in ward  = {'John Doe' in ward}")
    print()

    # __iter__ — used by for loops, list(), etc.
    print("__iter__     for patient in ward:")
    for patient in ward:
        print(f"  → {patient}")
    print()

    # __reversed__
    print("__reversed__ reversed(ward):")
    for patient in reversed(ward):
        print(f"  → {patient}")
    print()

    # __setitem__
    print("__setitem__  ward[1] = 'Eve Davis'")
    ward[1] = "Eve Davis"
    print(f"  ward[1] is now: {ward[1]}")
    print()

    # __delitem__
    print("__delitem__  del ward[0]")
    del ward[0]
    print()

    # State after modifications
    print("Current ward state:")
    print(ward)
    print()
    print(repr(ward))

