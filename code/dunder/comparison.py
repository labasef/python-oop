"""
Dunder Methods: Comparison Operators
__eq__, __ne__, __lt__, __le__, __gt__, __ge__, __hash__

- __eq__   : ==   (equality)
- __ne__   : !=   (inequality — auto-derived from __eq__ if not defined)
- __lt__   : <    (less than)
- __le__   : <=   (less than or equal)
- __gt__   : >    (greater than)
- __ge__   : >=   (greater than or equal)
- __hash__ : hash(obj) — must be defined alongside __eq__

Medical theme: Patient vital signs and triage priority system.
"""

from functools import total_ordering


@total_ordering
class VitalSigns:
    """
    Records a patient's vital signs at a point in time.

    @total_ordering from functools is a convenience decorator:
    define __eq__ and ONE of __lt__/__gt__/__le__/__ge__ and it will
    automatically derive the remaining three comparison methods.

    Here we compare vital signs by severity score — higher means more critical.
    """

    def __init__(
        self,
        patient_name: str,
        heart_rate: int,        # bpm
        systolic_bp: int,       # mmHg
        oxygen_saturation: float,  # %
        temperature: float,     # °C
    ):
        self.patient_name = patient_name
        self.heart_rate = heart_rate
        self.systolic_bp = systolic_bp
        self.oxygen_saturation = oxygen_saturation
        self.temperature = temperature

    @property
    def severity_score(self) -> int:
        """
        Simple triage score (higher = more critical).
        In a real system this would be a validated clinical tool (e.g. NEWS2).
        """
        score = 0
        if self.heart_rate > 100 or self.heart_rate < 50:
            score += 2
        if self.systolic_bp > 160 or self.systolic_bp < 90:
            score += 2
        if self.oxygen_saturation < 95:
            score += 3
        if self.temperature > 38.5 or self.temperature < 36.0:
            score += 1
        return score

    # ------------------------------------------------------------------
    # __eq__  — defines what "equal severity" means
    # Defining __eq__ sets __hash__ to None by default; we restore it below.
    # ------------------------------------------------------------------
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VitalSigns):
            return NotImplemented
        return self.severity_score == other.severity_score

    # ------------------------------------------------------------------
    # __lt__  — combined with @total_ordering, this is all we need
    # ------------------------------------------------------------------
    def __lt__(self, other: "VitalSigns") -> bool:
        if not isinstance(other, VitalSigns):
            return NotImplemented
        return self.severity_score < other.severity_score

    # ------------------------------------------------------------------
    # __hash__  — required because we defined __eq__
    # Objects used as dict keys or in sets must be hashable.
    # ------------------------------------------------------------------
    def __hash__(self) -> int:
        return hash((self.patient_name, self.severity_score))

    def __repr__(self) -> str:
        return (
            f"VitalSigns({self.patient_name!r}, "
            f"hr={self.heart_rate}, bp={self.systolic_bp}, "
            f"o2={self.oxygen_saturation}%, temp={self.temperature}°C, "
            f"score={self.severity_score})"
        )

    def __str__(self) -> str:
        return (
            f"{self.patient_name}: "
            f"HR={self.heart_rate}bpm  BP={self.systolic_bp}mmHg  "
            f"O₂={self.oxygen_saturation}%  Temp={self.temperature}°C  "
            f"[severity={self.severity_score}]"
        )


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Comparison Dunders: Patient Triage ===\n")

    stable   = VitalSigns("Alice Smith",  72,  118, 98.5, 36.8)  # score 0
    elevated = VitalSigns("Bob Johnson",  105, 165, 96.0, 38.7)  # score 5
    critical = VitalSigns("Carol White", 130,  80,  89.0, 39.2)  # score 8

    print("Patient vital signs:")
    for v in [stable, elevated, critical]:
        print(f"  {v}")
    print()

    # __eq__ and __ne__
    print("--- Equality (==, !=) ---")
    print(f"stable == elevated  : {stable == elevated}")
    print(f"stable != elevated  : {stable != elevated}")
    print()

    # __lt__, __le__, __gt__, __ge__ (derived by @total_ordering)
    print("--- Ordering (<, <=, >, >=) ---")
    print(f"stable < elevated   : {stable < elevated}")
    print(f"critical > elevated : {critical > elevated}")
    print(f"stable <= stable    : {stable <= stable}")
    print(f"critical >= elevated: {critical >= elevated}")
    print()

    # Sorting — uses __lt__ under the hood
    print("--- Triage order (sorted by severity, most critical last) ---")
    patients = [elevated, critical, stable]
    for v in sorted(patients):
        print(f"  {v}")
    print()

    # Most critical — uses __gt__ via max()
    print("--- Most critical patient ---")
    print(f"  {max(patients)}")
    print()

    # __hash__ — allows use in sets and as dict keys
    print("--- Using VitalSigns in a set (requires __hash__) ---")
    seen = {stable, elevated, critical}
    print(f"  Unique severity records: {len(seen)}")

