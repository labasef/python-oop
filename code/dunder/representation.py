"""
Dunder Methods: String Representation
__str__, __repr__, __format__

- __str__    : Human-readable string, used by print() and str()
- __repr__   : Unambiguous developer string, used in REPL and repr()
- __format__ : Controls how the object responds to format() and f-strings

Medical theme: Prescription and dosage records.
"""


class Medication:
    """
    A medication with prescribed dosage.

    __repr__ should ideally be a string that, when passed to eval(),
    would recreate the object:  eval(repr(obj)) == obj
    __str__ is meant for end-users and can be more descriptive.
    __format__ lets you choose different display formats via format specs.
    """

    def __init__(self, name: str, dosage_mg: float, frequency: str):
        self.name = name
        self.dosage_mg = dosage_mg
        self.frequency = frequency  # e.g. "twice daily"

    # ------------------------------------------------------------------
    # __repr__
    # Goal: a string a developer can use to recreate the object.
    # Shown in the REPL, in lists, and as a fallback when __str__ is absent.
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"Medication(name={self.name!r}, "
            f"dosage_mg={self.dosage_mg}, "
            f"frequency={self.frequency!r})"
        )

    # ------------------------------------------------------------------
    # __str__
    # Goal: a readable string for end-users (doctors, nurses, patients).
    # Used by print() and str().
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        return f"{self.name} {self.dosage_mg}mg — {self.frequency}"

    # ------------------------------------------------------------------
    # __format__
    # Goal: respond to format specifiers in format() / f-strings.
    #   format(med, "short")  → "Ibuprofen 400mg"
    #   format(med, "full")   → full prescription label
    #   format(med, "")       → falls back to __str__
    # ------------------------------------------------------------------
    def __format__(self, spec: str) -> str:
        if spec == "short":
            return f"{self.name} {self.dosage_mg}mg"
        if spec == "full":
            return (
                f"PRESCRIPTION\n"
                f"  Drug      : {self.name}\n"
                f"  Dosage    : {self.dosage_mg} mg\n"
                f"  Frequency : {self.frequency}"
            )
        # Default: same as __str__
        return str(self)


class Prescription:
    """
    A full prescription for a patient.
    Demonstrates how __repr__ and __str__ work for a container class.
    """

    def __init__(self, patient_name: str, doctor_name: str):
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.medications: list[Medication] = []

    def add_medication(self, medication: Medication):
        self.medications.append(medication)

    def __repr__(self) -> str:
        return (
            f"Prescription(patient={self.patient_name!r}, "
            f"doctor={self.doctor_name!r}, "
            f"medications={self.medications!r})"
        )

    def __str__(self) -> str:
        lines = [
            f"Prescription for {self.patient_name}",
            f"Prescribed by Dr. {self.doctor_name}",
            "Medications:",
        ]
        for med in self.medications:
            lines.append(f"  • {med}")  # calls med.__str__()
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Representation Dunders: Prescriptions ===\n")

    ibuprofen  = Medication("Ibuprofen",   400.0, "three times daily")
    amoxicillin = Medication("Amoxicillin", 500.0, "twice daily")

    # __str__ — called by print()
    print("__str__ output (print):")
    print(ibuprofen)
    print(amoxicillin)
    print()

    # __repr__ — called by repr() and shown in REPL / containers
    print("__repr__ output:")
    print(repr(ibuprofen))
    print()

    # __repr__ is used when an object appears inside a list
    print("Objects inside a list (uses __repr__):")
    print([ibuprofen, amoxicillin])
    print()

    # __format__ — custom format specs via format() and f-strings
    print("__format__ — short spec:")
    print(format(ibuprofen, "short"))
    print()

    print("__format__ — full spec:")
    print(f"{amoxicillin:full}")
    print()

    # Prescription uses __str__ of its medications
    rx = Prescription("Alice Brown", "Sarah Chen")
    rx.add_medication(ibuprofen)
    rx.add_medication(amoxicillin)

    print("__str__ of Prescription:")
    print(rx)
    print()

    print("__repr__ of Prescription:")
    print(repr(rx))

