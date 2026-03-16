"""
Mixin Pattern Example

Mixins are classes that provide reusable functionality to be mixed into other classes.

This example demonstrates adding capabilities (logging, serialization, validation)
to medical records without deep inheritance.
"""


class LogMixin:
    """Mixin - Adds logging capability to any class."""
    
    def log(self, message: str):
        """Log a message with the class name."""
        print(f"[{self.__class__.__name__}] {message}")


class SerializeMixin:
    """Mixin - Adds serialization capability to any class."""
    
    def serialize(self) -> dict:
        """Convert object attributes to dictionary."""
        return {
            k: v for k, v in self.__dict__.items() 
            if not k.startswith('_')
        }
    
    def to_json_string(self) -> str:
        """Convert to JSON-like string representation."""
        data = self.serialize()
        items = [f'"{k}": "{v}"' for k, v in data.items()]
        return "{" + ", ".join(items) + "}"


class ValidationMixin:
    """Mixin - Adds validation capability to any class."""
    
    def validate(self, *required_fields: str) -> bool:
        """Validate that required fields are present and non-empty."""
        missing = [f for f in required_fields if not getattr(self, f, None)]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
        return True


class AuditMixin:
    """Mixin - Adds audit trail capability to any class."""
    
    def __init__(self, *args, **kwargs):
        self._audit_trail = []
        super().__init__(*args, **kwargs)
    
    def record_action(self, action: str, details: str = ""):
        """Record an action in the audit trail."""
        entry = f"Action: {action}"
        if details:
            entry += f" | {details}"
        self._audit_trail.append(entry)
    
    def get_audit_trail(self) -> list:
        """Retrieve the audit trail."""
        return list(self._audit_trail)


class PatientRecord(LogMixin, SerializeMixin, ValidationMixin):
    """Patient record with logging, serialization, and validation."""
    
    def __init__(self, patient_id: str, name: str, age: int):
        self.patient_id = patient_id
        self.name = name
        self.age = age
    
    def admit(self):
        """Admit patient."""
        self.validate("patient_id", "name", "age")
        self.log(f"Admitting patient {self.name}")


class MedicationRecord(LogMixin, SerializeMixin, ValidationMixin, AuditMixin):
    """Medication record with all capabilities."""
    
    def __init__(self, medication_id: str, medication_name: str, dosage: str):
        self.medication_id = medication_id
        self.medication_name = medication_name
        self.dosage = dosage
        self._audit_trail = []
    
    def administer(self, patient_name: str):
        """Administer medication."""
        self.validate("medication_id", "medication_name", "dosage")
        self.log(f"Administering {self.medication_name} ({self.dosage}) to {patient_name}")
        self.record_action("administer", f"Patient: {patient_name}")
    
    def modify_dosage(self, new_dosage: str):
        """Modify medication dosage."""
        old_dosage = self.dosage
        self.dosage = new_dosage
        self.log(f"Dosage changed from {old_dosage} to {new_dosage}")
        self.record_action("modify_dosage", f"{old_dosage} → {new_dosage}")


class LabResult(LogMixin, SerializeMixin, ValidationMixin, AuditMixin):
    """Lab result record with full capabilities."""
    
    def __init__(self, test_id: str, test_type: str, result: str):
        self.test_id = test_id
        self.test_type = test_type
        self.result = result
        self._audit_trail = []
    
    def process_result(self):
        """Process lab result."""
        self.validate("test_id", "test_type", "result")
        self.log(f"Processing {self.test_type}: {self.result}")
        self.record_action("process_result", f"Result: {self.result}")


# Example usage
if __name__ == "__main__":
    print("=== Mixin Pattern Example: Medical Records ===\n")
    
    # Patient Record (LogMixin, SerializeMixin, ValidationMixin)
    print("--- Patient Record ---")
    patient = PatientRecord("P001", "Alice Smith", 45)
    patient.admit()
    print(f"Serialized: {patient.to_json_string()}\n")
    
    # Medication Record (all mixins including AuditMixin)
    print("--- Medication Record ---")
    medication = MedicationRecord("M123", "Ibuprofen", "400mg")
    medication.administer("Alice Smith")
    medication.modify_dosage("600mg")
    print(f"Serialized: {medication.to_json_string()}")
    print(f"Audit Trail: {medication.get_audit_trail()}\n")
    
    # Lab Result (all mixins including AuditMixin)
    print("--- Lab Result ---")
    lab = LabResult("L456", "Blood Work", "Normal")
    lab.process_result()
    print(f"Serialized: {lab.to_json_string()}")
    print(f"Audit Trail: {lab.get_audit_trail()}\n")
    
    print("=== End of Example ===")

