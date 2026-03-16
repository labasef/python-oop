"""
Dunder Methods: Arithmetic Operators
__add__, __sub__, __mul__, __truediv__, __floordiv__, __mod__,
__iadd__, __isub__, __neg__, __abs__, __round__

- __add__      : +
- __sub__      : -
- __mul__      : *
- __truediv__  : /
- __floordiv__ : //
- __mod__      : %
- __iadd__     : +=   (in-place add)
- __isub__     : -=   (in-place subtract)
- __neg__      : unary -  (e.g. -dose)
- __abs__      : abs()
- __round__    : round()

Medical theme: Drug dosage calculations and fluid balance records.
"""


class Dosage:
    """
    Represents a medication dosage in milligrams.

    Supports arithmetic so dosages can be combined, scaled, or compared
    naturally without extracting the raw number each time.
    """

    def __init__(self, amount_mg: float, unit: str = "mg"):
        if amount_mg < 0:
            raise ValueError("Dosage cannot be negative")
        self.amount_mg = float(amount_mg)
        self.unit = unit

    # ------------------------------------------------------------------
    # Binary arithmetic operators
    # ------------------------------------------------------------------
    def __add__(self, other: "Dosage") -> "Dosage":
        """dose1 + dose2 — combine two dosages."""
        if not isinstance(other, Dosage):
            return NotImplemented
        return Dosage(self.amount_mg + other.amount_mg, self.unit)

    def __sub__(self, other: "Dosage") -> "Dosage":
        """dose1 - dose2 — subtract one dosage from another."""
        if not isinstance(other, Dosage):
            return NotImplemented
        result = self.amount_mg - other.amount_mg
        if result < 0:
            raise ValueError("Resulting dosage cannot be negative")
        return Dosage(result, self.unit)

    def __mul__(self, factor: float) -> "Dosage":
        """dose * 3 — scale dosage (e.g. total over 3 days)."""
        if not isinstance(factor, (int, float)):
            return NotImplemented
        return Dosage(self.amount_mg * factor, self.unit)

    def __rmul__(self, factor: float) -> "Dosage":
        """3 * dose — supports multiplication from the left side."""
        return self.__mul__(factor)

    def __truediv__(self, divisor: float) -> "Dosage":
        """dose / 2 — split dosage (e.g. divide daily dose into two)."""
        if divisor == 0:
            raise ZeroDivisionError("Cannot divide dosage by zero")
        return Dosage(self.amount_mg / divisor, self.unit)

    def __floordiv__(self, divisor: int) -> "Dosage":
        """dose // 3 — integer division (whole-number doses)."""
        return Dosage(self.amount_mg // divisor, self.unit)

    def __mod__(self, divisor: float) -> "Dosage":
        """dose % 100 — remainder (e.g. what's left after rounding to 100mg)."""
        return Dosage(self.amount_mg % divisor, self.unit)

    # ------------------------------------------------------------------
    # In-place operators — modify self and return self
    # ------------------------------------------------------------------
    def __iadd__(self, other: "Dosage") -> "Dosage":
        """dose += extra — add to existing dosage in place."""
        if not isinstance(other, Dosage):
            return NotImplemented
        self.amount_mg += other.amount_mg
        return self

    def __isub__(self, other: "Dosage") -> "Dosage":
        """dose -= reduction — subtract from existing dosage in place."""
        if not isinstance(other, Dosage):
            return NotImplemented
        self.amount_mg -= other.amount_mg
        if self.amount_mg < 0:
            raise ValueError("Resulting dosage cannot be negative")
        return self

    # ------------------------------------------------------------------
    # Unary operators
    # ------------------------------------------------------------------
    def __neg__(self) -> "Dosage":
        """-dose — not clinically meaningful, but shows the pattern."""
        raise ValueError("A dosage cannot be negated — use subtraction instead")

    def __abs__(self) -> "Dosage":
        """abs(dose) — return absolute value (always positive)."""
        return Dosage(abs(self.amount_mg), self.unit)

    def __round__(self, ndigits: int = 0) -> "Dosage":
        """round(dose, 1) — round to nearest significant amount."""
        return Dosage(round(self.amount_mg, ndigits), self.unit)

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return f"Dosage({self.amount_mg}{self.unit})"

    def __str__(self) -> str:
        return f"{self.amount_mg}{self.unit}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dosage):
            return NotImplemented
        return self.amount_mg == other.amount_mg

    def __hash__(self) -> int:
        return hash(self.amount_mg)


class FluidBalance:
    """
    Tracks a patient's fluid intake and output in millilitres.

    Demonstrates __iadd__ and __isub__ in a realistic clinical context.
    """

    def __init__(self, patient_name: str):
        self.patient_name = patient_name
        self.intake_ml = 0.0
        self.output_ml = 0.0

    @property
    def balance_ml(self) -> float:
        return self.intake_ml - self.output_ml

    def __iadd__(self, intake: float) -> "FluidBalance":
        """balance += 250  — record fluid intake."""
        self.intake_ml += intake
        print(f"  [+{intake}ml intake] Running balance: {self.balance_ml:+.0f}ml")
        return self

    def __isub__(self, output: float) -> "FluidBalance":
        """balance -= 300  — record fluid output."""
        self.output_ml += output
        print(f"  [-{output}ml output] Running balance: {self.balance_ml:+.0f}ml")
        return self

    def __str__(self) -> str:
        return (
            f"{self.patient_name} — "
            f"In: {self.intake_ml}ml  Out: {self.output_ml}ml  "
            f"Balance: {self.balance_ml:+.0f}ml"
        )


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Arithmetic Dunders: Dosage Calculations ===\n")

    morning  = Dosage(400, "mg")  # 400mg morning dose
    evening  = Dosage(200, "mg")  # 200mg evening dose

    # __add__
    print(f"Morning + Evening  = {morning + evening}")

    # __sub__
    print(f"Morning - Evening  = {morning - evening}")

    # __mul__ and __rmul__
    print(f"Morning * 7 days   = {morning * 7}")
    print(f"7 days * Morning   = {7 * morning}")

    # __truediv__
    print(f"Morning / 2        = {morning / 2}")

    # __floordiv__ and __mod__
    large = Dosage(750, "mg")
    print(f"750mg // 100       = {large // 100}")
    print(f"750mg %  100       = {large % 100}")

    # __round__
    precise = Dosage(312.666, "mg")
    print(f"round(312.666mg,1) = {round(precise, 1)}")
    print()

    # __iadd__ and __isub__
    print("--- In-place operators ---")
    daily = Dosage(400, "mg")
    print(f"Starting dose: {daily}")
    daily += Dosage(100, "mg")
    print(f"After +=100mg: {daily}")
    daily -= Dosage(50, "mg")
    print(f"After -=50mg:  {daily}")
    print()

    # FluidBalance — clinical __iadd__ / __isub__
    print("=== Arithmetic Dunders: Fluid Balance ===\n")
    fb = FluidBalance("John Smith")
    fb += 500   # IV drip
    fb += 250   # oral intake
    fb -= 400   # urine output
    fb -= 100   # nasogastric drainage
    fb += 150   # oral intake
    print(f"\nSummary: {fb}")

