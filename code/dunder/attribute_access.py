"""
Dunder Methods: Attribute Access
__getattr__, __getattribute__, __setattr__, __delattr__

- __getattribute__ : Called on EVERY attribute access — obj.anything
- __getattr__      : Called ONLY when the attribute is NOT found normally
                     (fallback after __getattribute__ raises AttributeError)
- __setattr__      : Called on EVERY attribute assignment — obj.x = value
- __delattr__      : Called when an attribute is deleted — del obj.x

Key distinction:
  __getattribute__ intercepts ALL reads  (use carefully — infinite loops possible)
  __getattr__      intercepts only MISSING attribute reads (safer fallback hook)

Medical theme: Electronic Health Record (EHR) with access control and audit logging.
"""


class EHR:
    """
    Electronic Health Record with attribute access control.

    Demonstrates:
    - __setattr__  : Validate and log every field assignment
    - __getattr__  : Return a helpful message for unknown fields
    - __delattr__  : Prevent deletion of critical fields
    """

    # Fields that cannot be deleted once set
    _PROTECTED = frozenset({"patient_id", "name"})

    # Fields whose values must be non-empty strings
    _REQUIRED_STR = frozenset({"patient_id", "name", "blood_type"})

    def __init__(self, patient_id: str, name: str, blood_type: str = "Unknown"):
        # Use object.__setattr__ to bypass our own __setattr__ during init
        object.__setattr__(self, "_access_log", [])
        object.__setattr__(self, "patient_id", patient_id)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "blood_type", blood_type)
        object.__setattr__(self, "notes", [])

    # ------------------------------------------------------------------
    # __setattr__ — intercepts ALL assignments
    # ------------------------------------------------------------------
    def __setattr__(self, name: str, value):
        """
        Validate and log every attribute assignment.
        Must call object.__setattr__ to actually store the value,
        otherwise this method would call itself recursively.
        """
        if name in self._REQUIRED_STR and not isinstance(value, str):
            raise TypeError(f"Field '{name}' must be a non-empty string")
        if name in self._REQUIRED_STR and not value:
            raise ValueError(f"Field '{name}' cannot be empty")

        self._access_log.append(f"SET  {name} = {value!r}")
        object.__setattr__(self, name, value)

    # ------------------------------------------------------------------
    # __getattr__ — called ONLY for attributes that don't exist
    # ------------------------------------------------------------------
    def __getattr__(self, name: str):
        """
        Fallback for any attribute not found through normal lookup.
        Note: __getattr__ is NOT called for attributes that DO exist —
        those are found by __getattribute__ (the default machinery).
        """
        self._access_log.append(f"GET  {name} (NOT FOUND)")
        return f"[EHR] Field '{name}' is not recorded for {self.name}"

    # ------------------------------------------------------------------
    # __delattr__ — intercepts del obj.field
    # ------------------------------------------------------------------
    def __delattr__(self, name: str):
        """Prevent deletion of protected fields; allow others."""
        if name in self._PROTECTED:
            raise AttributeError(
                f"Cannot delete protected field '{name}' from EHR"
            )
        self._access_log.append(f"DEL  {name}")
        object.__delattr__(self, name)

    def get_access_log(self) -> list[str]:
        return list(self._access_log)

    def __repr__(self) -> str:
        return (
            f"EHR(id={self.patient_id!r}, name={self.name!r}, "
            f"blood_type={self.blood_type!r})"
        )


class AuditedVitals:
    """
    Patient vitals with __getattribute__ to log every single access.

    Use __getattribute__ sparingly — it fires on EVERY attribute read,
    including internal ones. Always call super().__getattribute__() to avoid
    infinite recursion.
    """

    def __init__(self, heart_rate: int, blood_pressure: str, temperature: float):
        self.heart_rate = heart_rate
        self.blood_pressure = blood_pressure
        self.temperature = temperature
        self._read_count: dict[str, int] = {}

    def __getattribute__(self, name: str):
        """
        Intercepts ALL attribute reads.
        We skip tracking private/dunder names and the counter itself
        to avoid infinite recursion.
        """
        value = super().__getattribute__(name)
        if not name.startswith("_"):
            # Safely increment the read counter without triggering recursion
            counter = super().__getattribute__("_read_count")
            counter[name] = counter.get(name, 0) + 1
        return value

    def access_report(self) -> str:
        lines = ["Field access counts:"]
        for field, count in self._read_count.items():
            lines.append(f"  {field}: accessed {count} time(s)")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Attribute Access Dunders: Electronic Health Record ===\n")

    print("--- Creating EHR ---")
    ehr = EHR("P1001", "Alice Brown", "A+")
    print(repr(ehr))
    print()

    print("--- __setattr__: updating fields ---")
    ehr.blood_type = "B+"
    ehr.diagnosis  = "Hypertension Stage 1"
    ehr.medication = "Lisinopril 10mg"
    print()

    print("--- __getattr__: accessing a field that doesn't exist ---")
    print(ehr.allergy_notes)   # not set — falls back to __getattr__
    print(ehr.surgical_history)
    print()

    print("--- __delattr__: deleting a non-protected field ---")
    del ehr.medication
    print("  medication deleted")
    print()

    print("--- __delattr__: trying to delete a protected field ---")
    try:
        del ehr.patient_id
    except AttributeError as e:
        print(f"  Blocked: {e}")
    print()

    print("--- __setattr__: invalid assignment ---")
    try:
        ehr.patient_id = ""
    except ValueError as e:
        print(f"  Blocked: {e}")
    print()

    print("--- EHR access log ---")
    for entry in ehr.get_access_log():
        print(f"  {entry}")
    print()

    print("=== Attribute Access Dunders: Audited Vitals ===\n")
    vitals = AuditedVitals(72, "120/80", 36.8)

    # Each access increments the counter
    _ = vitals.heart_rate
    _ = vitals.heart_rate
    _ = vitals.blood_pressure
    _ = vitals.temperature
    _ = vitals.heart_rate

    print(vitals.access_report())

