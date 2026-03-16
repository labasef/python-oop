"""
Context Manager Pattern Example

The Context Manager pattern manages resource allocation and cleanup.

This example demonstrates managing patient admission and discharge 
in a hospital context.
"""


class HospitalAdmission:
    """Context manager for hospital patient admission and discharge."""
    
    def __init__(self, patient_name: str, admission_reason: str):
        self.patient_name = patient_name
        self.admission_reason = admission_reason
        self.bed_number = None
        self.admission_time = None
        self.is_admitted = False
    
    def __enter__(self):
        """Setup: Admit patient to hospital."""
        self.is_admitted = True
        self.bed_number = 42  # Simulated bed assignment
        self.admission_time = "2026-03-16 10:30"
        
        print(f"✓ Patient {self.patient_name} admitted")
        print(f"  Reason: {self.admission_reason}")
        print(f"  Bed: {self.bed_number}")
        print(f"  Admission time: {self.admission_time}\n")
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup: Discharge patient from hospital."""
        self.is_admitted = False
        discharge_time = "2026-03-18 14:00"
        
        if exc_type:
            print(f"✗ Error during stay: {exc_val}")
        
        print(f"\n✓ Patient {self.patient_name} discharged")
        print(f"  Discharge time: {discharge_time}")
        print(f"  Bed {self.bed_number} now available")
        
        return False  # Don't suppress exceptions
    
    def administer_medication(self, medication: str, dosage: str):
        """Administer medication to patient."""
        if not self.is_admitted:
            raise RuntimeError("Patient is not admitted")
        print(f"→ Administered {dosage} of {medication}")
    
    def run_test(self, test_type: str):
        """Run medical test on patient."""
        if not self.is_admitted:
            raise RuntimeError("Patient is not admitted")
        print(f"→ Running {test_type}")
        return f"{test_type} results: normal"


class MedicationContext:
    """Context manager for medication administration with timing."""
    
    def __init__(self, patient_name: str, medication: str):
        self.patient_name = patient_name
        self.medication = medication
        self.start_time = None
    
    def __enter__(self):
        self.start_time = "14:00"
        print(f"→ Starting {self.medication} administration at {self.start_time}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = "14:30"
        print(f"→ Completed {self.medication} administration at {end_time}")
        if exc_type:
            print(f"  Warning: {exc_val}")
        return False


# Example usage
if __name__ == "__main__":
    print("=== Context Manager Pattern Example: Hospital Admission ===\n")
    
    # Using hospital admission context manager
    try:
        with HospitalAdmission("John Smith", "Acute appendicitis") as admission:
            print("=== Patient Care Procedures ===\n")
            
            admission.administer_medication("Antibiotics", "500mg")
            print(admission.run_test("Blood work"))
            print()
            
            # Medication administration with its own context
            with MedicationContext("John Smith", "Pain relief"):
                pass
            
            print("\n=== Patient in stable condition ===")
    
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n=== End of Example ===")

