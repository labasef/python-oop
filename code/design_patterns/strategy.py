"""
Strategy Pattern Example

The Strategy pattern defines a family of algorithms, encapsulates each one,
and makes them interchangeable.

This example demonstrates different medication prescription strategies
for treating patient conditions.
"""

from abc import ABC, abstractmethod


class TreatmentStrategy(ABC):
    """Abstract strategy for patient treatment."""
    
    @abstractmethod
    def treat(self, patient_name: str, condition: str) -> str:
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        pass


class MedicationStrategy(TreatmentStrategy):
    """Strategy - Treat with medication."""
    
    def __init__(self, medication: str, cost: float):
        self.medication = medication
        self.cost = cost
    
    def treat(self, patient_name: str, condition: str) -> str:
        return f"Prescribe {self.medication} to {patient_name} for {condition}"
    
    def get_cost(self) -> float:
        return self.cost


class TherapyStrategy(TreatmentStrategy):
    """Strategy - Treat with therapy."""
    
    def __init__(self, therapy_type: str, sessions: int, cost_per_session: float):
        self.therapy_type = therapy_type
        self.sessions = sessions
        self.cost_per_session = cost_per_session
    
    def treat(self, patient_name: str, condition: str) -> str:
        return f"Schedule {self.sessions} {self.therapy_type} sessions for {patient_name}'s {condition}"
    
    def get_cost(self) -> float:
        return self.sessions * self.cost_per_session


class SurgeryStrategy(TreatmentStrategy):
    """Strategy - Treat with surgery."""
    
    def __init__(self, surgery_type: str, cost: float):
        self.surgery_type = surgery_type
        self.cost = cost
    
    def treat(self, patient_name: str, condition: str) -> str:
        return f"Schedule {self.surgery_type} for {patient_name} to treat {condition}"
    
    def get_cost(self) -> float:
        return self.cost


class Doctor:
    """Doctor that uses different treatment strategies."""
    
    def __init__(self, name: str):
        self.name = name
        self.strategy = None
    
    def set_treatment_strategy(self, strategy: TreatmentStrategy):
        """Set the treatment strategy."""
        self.strategy = strategy
    
    def prescribe_treatment(self, patient_name: str, condition: str):
        """Prescribe treatment using the current strategy."""
        if self.strategy is None:
            raise ValueError("No treatment strategy selected")
        
        treatment = self.strategy.treat(patient_name, condition)
        cost = self.strategy.get_cost()
        print(f"Dr. {self.name}: {treatment}")
        print(f"  Estimated cost: £{cost:.2f}\n")


# Example usage
if __name__ == "__main__":
    print("=== Strategy Pattern Example: Medical Treatment Planning ===\n")
    
    doctor = Doctor("Sarah Chen")
    patient = "Robert Johnson"
    
    # Treat back pain with medication strategy
    print("--- Treating back pain ---")
    doctor.set_treatment_strategy(
        MedicationStrategy("Ibuprofen 400mg", 15.00)
    )
    doctor.prescribe_treatment(patient, "back pain")
    
    # Treat knee injury with therapy strategy
    print("--- Treating knee injury ---")
    doctor.set_treatment_strategy(
        TherapyStrategy("physical therapy", 6, 75.00)
    )
    doctor.prescribe_treatment(patient, "knee injury")
    
    # Treat appendicitis with surgery strategy
    print("--- Treating appendicitis ---")
    doctor.set_treatment_strategy(
        SurgeryStrategy("appendectomy", 3500.00)
    )
    doctor.prescribe_treatment(patient, "appendicitis")
    
    print("=== End of Example ===")

