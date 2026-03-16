"""
Decorator Pattern Example

The Decorator pattern attaches additional responsibilities to an object dynamically.

This example demonstrates adding features to patient records (base object) 
dynamically without modifying the original class.
"""

from abc import ABC, abstractmethod


class PatientRecord(ABC):
    """Abstract PatientRecord interface."""
    
    @abstractmethod
    def get_details(self) -> str:
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        pass


class BasicPatientRecord(PatientRecord):
    """Concrete - Basic patient record."""
    
    def __init__(self, patient_name: str, patient_id: str):
        self.patient_name = patient_name
        self.patient_id = patient_id
    
    def get_details(self) -> str:
        return f"Patient: {self.patient_name} (ID: {self.patient_id})"
    
    def get_cost(self) -> float:
        return 0.0


class PatientRecordDecorator(PatientRecord):
    """Base decorator for patient records."""
    
    def __init__(self, patient_record: PatientRecord):
        self.patient_record = patient_record
    
    def get_details(self) -> str:
        return self.patient_record.get_details()
    
    def get_cost(self) -> float:
        return self.patient_record.get_cost()


class LabTestDecorator(PatientRecordDecorator):
    """Decorator - Adds lab test information."""
    
    def __init__(self, patient_record: PatientRecord, test_type: str, cost: float = 50.0):
        super().__init__(patient_record)
        self.test_type = test_type
        self.test_cost = cost
    
    def get_details(self) -> str:
        return f"{self.patient_record.get_details()}\n  + Lab Test: {self.test_type}"
    
    def get_cost(self) -> float:
        return self.patient_record.get_cost() + self.test_cost


class ImagingDecorator(PatientRecordDecorator):
    """Decorator - Adds imaging information."""
    
    def __init__(self, patient_record: PatientRecord, imaging_type: str, cost: float = 200.0):
        super().__init__(patient_record)
        self.imaging_type = imaging_type
        self.imaging_cost = cost
    
    def get_details(self) -> str:
        return f"{self.patient_record.get_details()}\n  + Imaging: {self.imaging_type}"
    
    def get_cost(self) -> float:
        return self.patient_record.get_cost() + self.imaging_cost


class VaccinationDecorator(PatientRecordDecorator):
    """Decorator - Adds vaccination information."""
    
    def __init__(self, patient_record: PatientRecord, vaccine: str, cost: float = 30.0):
        super().__init__(patient_record)
        self.vaccine = vaccine
        self.vaccine_cost = cost
    
    def get_details(self) -> str:
        return f"{self.patient_record.get_details()}\n  + Vaccination: {self.vaccine}"
    
    def get_cost(self) -> float:
        return self.patient_record.get_cost() + self.vaccine_cost


# Example usage
if __name__ == "__main__":
    print("=== Decorator Pattern Example: Patient Medical Records ===\n")
    
    # Create a basic patient record
    patient = BasicPatientRecord("Alice Brown", "P12345")
    print(patient.get_details())
    print(f"Cost: £{patient.get_cost():.2f}\n")
    
    # Add lab test dynamically
    print("--- Adding lab test ---")
    patient = LabTestDecorator(patient, "Blood Work", 60.0)
    print(patient.get_details())
    print(f"Cost: £{patient.get_cost():.2f}\n")
    
    # Add imaging dynamically
    print("--- Adding imaging ---")
    patient = ImagingDecorator(patient, "X-Ray", 150.0)
    print(patient.get_details())
    print(f"Cost: £{patient.get_cost():.2f}\n")
    
    # Add vaccination dynamically
    print("--- Adding vaccination ---")
    patient = VaccinationDecorator(patient, "COVID-19 Booster", 25.0)
    print(patient.get_details())
    print(f"Total Cost: £{patient.get_cost():.2f}\n")
    
    print("=== End of Example ===")

