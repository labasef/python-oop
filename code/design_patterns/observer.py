"""
Observer Pattern Example

The Observer pattern is a behavioral design pattern that defines a one-to-many 
relationship between objects so that when one object (subject) changes state, 
all its dependents (observers) are notified automatically.

This example demonstrates a health monitoring system where multiple observers
(doctors, nurses, family) are notified when a patient's health status changes.
"""


class Observer:
    """Abstract observer class that defines the interface for observers."""
    def update(self, patient, *args, **kwargs):
        raise NotImplementedError


class Doctor(Observer):
    """Concrete observer - Doctor is notified of patient changes."""
    def __init__(self, name):
        self.name = name
    
    def update(self, patient, *args, **kwargs):
        print(f"Doctor {self.name}: Patient {patient.id} status changed - "
              f"Illness: {patient.illness}, Days ill: {patient.days_ill}")


class Nurse(Observer):
    """Concrete observer - Nurse is notified of patient changes."""
    def __init__(self, name):
        self.name = name
    
    def update(self, patient, *args, **kwargs):
        if patient.illness:
            print(f"Nurse {self.name}: Patient {patient.id} needs medical attention!")


class Family(Observer):
    """Concrete observer - Family member is notified of patient changes."""
    def __init__(self, name):
        self.name = name
    
    def update(self, patient, *args, **kwargs):
        if patient.illness:
            print(f"Family member {self.name}: Concerned about patient {patient.id}")
        else:
            print(f"Family member {self.name}: Patient {patient.id} is recovering well!")


class Patient:
    """Subject class - Patient whose state changes trigger notifications."""
    def __init__(self, patient_id):
        self.id = patient_id
        self.observers = []
        self.illness = False
        self.days_ill = 0
        self.interactions = []
    
    def attach_observer(self, observer):
        """Add an observer to the list."""
        if observer not in self.observers:
            self.observers.append(observer)
    
    def detach_observer(self, observer):
        """Remove an observer from the list."""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify_observers(self, *args, **kwargs):
        """Notify all observers of state change."""
        for observer in self.observers:
            observer.update(self, *args, **kwargs)
    
    def falls_ill(self):
        """Set patient as ill and notify observers."""
        self.illness = True
        self.days_ill = 1
        self.notify_observers()
    
    def get_worse(self):
        """Patient condition worsens."""
        if self.illness:
            self.days_ill += 1
            self.notify_observers()
    
    def recovers(self):
        """Patient recovers and notify observers."""
        self.illness = False
        self.days_ill = 0
        self.notify_observers()


# Example usage
if __name__ == "__main__":
    print("=== Observer Pattern Example: Health Monitoring System ===\n")
    
    # Create a patient
    patient = Patient(patient_id=101)
    
    # Create observers
    doctor = Doctor("Dr. Smith")
    nurse = Nurse("Nurse Johnson")
    family = Family("John (Son)")
    
    # Attach observers to patient
    patient.attach_observer(doctor)
    patient.attach_observer(nurse)
    patient.attach_observer(family)
    
    print("Patient registered with monitoring system\n")
    
    # Patient falls ill
    print("--- Patient falls ill ---")
    patient.falls_ill()
    print()
    
    # Patient condition worsens
    print("--- Patient's condition worsens ---")
    patient.get_worse()
    print()
    
    # Remove nurse observer
    print("--- Nurse goes off duty ---")
    patient.detach_observer(nurse)
    patient.get_worse()
    print()
    
    # Patient recovers
    print("--- Patient recovers ---")
    patient.recovers()
    print()
    
    print("=== End of Example ===")
