"""
Dunder Methods: Callable Objects
__call__

- __call__ : Makes an instance callable like a function — obj(args)

When a class defines __call__, its instances can be invoked with parentheses.
This is useful for:
- Stateful functions (the object holds context between calls)
- Strategy objects that need to be called repeatedly
- Function-like objects with configuration

Medical theme: Drug dosage calculators and clinical rule engines.
"""


class WeightBasedDosageCalculator:
    """
    Calculates weight-based drug dosages.

    Configuring a calculator once and then calling it multiple times
    is a natural use of __call__: the configuration (drug, mg-per-kg
    limits) is stored on the instance; the call itself takes patient data.
    """

    def __init__(
        self,
        drug_name: str,
        mg_per_kg: float,
        min_dose_mg: float,
        max_dose_mg: float,
    ):
        self.drug_name   = drug_name
        self.mg_per_kg   = mg_per_kg
        self.min_dose_mg = min_dose_mg
        self.max_dose_mg = max_dose_mg

    def __call__(self, patient_name: str, weight_kg: float) -> dict:
        """
        Calculate the appropriate dose for a patient.

        Usage:
            calc = WeightBasedDosageCalculator("Amoxicillin", 25, 250, 500)
            result = calc("Alice", 60)    ← __call__ invoked here
        """
        raw_dose = self.mg_per_kg * weight_kg
        clamped  = max(self.min_dose_mg, min(raw_dose, self.max_dose_mg))

        result = {
            "patient":  patient_name,
            "drug":     self.drug_name,
            "weight_kg": weight_kg,
            "raw_dose_mg":     round(raw_dose, 1),
            "prescribed_mg":   round(clamped, 1),
            "capped": clamped != raw_dose,
        }
        return result

    def __repr__(self) -> str:
        return (
            f"WeightBasedDosageCalculator({self.drug_name!r}, "
            f"{self.mg_per_kg}mg/kg, "
            f"range=[{self.min_dose_mg}–{self.max_dose_mg}mg])"
        )


class AlertThresholdChecker:
    """
    A configurable clinical alert checker.

    Stores the thresholds once; calling the instance tests a value and
    returns an alert level.  This pattern is common for rule engines where
    the rules are set up at startup and evaluated repeatedly at runtime.
    """

    LEVELS = {0: "NORMAL", 1: "CAUTION", 2: "WARNING", 3: "CRITICAL"}

    def __init__(self, metric: str, low_warn: float, low_crit: float,
                 high_warn: float, high_crit: float, unit: str = ""):
        self.metric    = metric
        self.low_warn  = low_warn
        self.low_crit  = low_crit
        self.high_warn = high_warn
        self.high_crit = high_crit
        self.unit      = unit
        self._call_count = 0

    def __call__(self, value: float, patient: str = "Patient") -> str:
        """Evaluate a measurement and return an alert message."""
        self._call_count += 1

        if value <= self.low_crit or value >= self.high_crit:
            level = 3
        elif value <= self.low_warn or value >= self.high_warn:
            level = 2
        else:
            level = 0

        label = self.LEVELS[level]
        return (
            f"[{label}] {patient}: {self.metric} = {value}{self.unit}"
        )

    @property
    def evaluations(self) -> int:
        return self._call_count

    def __repr__(self) -> str:
        return (
            f"AlertThresholdChecker({self.metric!r}, "
            f"warn=[{self.low_warn}–{self.high_warn}], "
            f"crit=[{self.low_crit}–{self.high_crit}]{self.unit})"
        )


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Callable Dunders (__call__): Medical Calculators ===\n")

    # Configure the calculator once
    amoxicillin_calc = WeightBasedDosageCalculator(
        drug_name="Amoxicillin",
        mg_per_kg=25,
        min_dose_mg=250,
        max_dose_mg=500,
    )
    print(f"Calculator: {amoxicillin_calc}\n")

    # Call the instance like a function for each patient
    patients = [
        ("Alice Smith",  8.0),   # child — likely hits min
        ("Bob Johnson",  70.0),  # adult — likely hits max
        ("Carol White",  18.0),  # adolescent — within range
    ]

    print("--- Dosage calculations ---")
    for name, weight in patients:
        result = amoxicillin_calc(name, weight)   # __call__
        cap_note = " (dose capped)" if result["capped"] else ""
        print(
            f"  {result['patient']:15s} ({result['weight_kg']}kg) "
            f"→ {result['prescribed_mg']}mg{cap_note}"
        )
    print()

    # Alert threshold checkers
    heart_rate_alert = AlertThresholdChecker(
        "Heart Rate", low_warn=50, low_crit=40,
        high_warn=100, high_crit=130, unit="bpm"
    )
    spo2_alert = AlertThresholdChecker(
        "SpO₂", low_warn=94, low_crit=90,
        high_warn=100, high_crit=100, unit="%"
    )

    print("--- Clinical alert checks ---")
    readings = [
        ("Alice Smith",  72,  98),
        ("Bob Johnson",  45,  93),   # low HR + low SpO₂
        ("Carol White",  135, 97),   # critical HR
    ]

    for name, hr, spo2 in readings:
        print(f"  {heart_rate_alert(hr, name)}")
        print(f"  {spo2_alert(spo2, name)}")
        print()

    print(f"Heart rate checker called {heart_rate_alert.evaluations} time(s)")
    print(f"SpO₂ checker called       {spo2_alert.evaluations} time(s)")

