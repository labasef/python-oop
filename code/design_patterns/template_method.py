"""
Template Method Pattern Example

The Template Method pattern defines the skeleton of an algorithm in the base 
class, letting subclasses implement specific steps.

This example demonstrates a patient diagnosis and treatment workflow.
"""

from abc import ABC, abstractmethod


class DiagnosisProcess(ABC):
    """Template method pattern - Diagnosis workflow."""
    
    def diagnose_patient(self, patient_name: str) -> str:
        """
        Template method - defines the skeleton of the diagnosis process.
        Concrete subclasses implement specific steps.
        """
        self.collect_symptoms(patient_name)
        self.examine_patient(patient_name)
        diagnosis = self.perform_tests(patient_name)
        treatment = self.create_treatment_plan(patient_name, diagnosis)
        return treatment
    
    @abstractmethod
    def collect_symptoms(self, patient_name: str):
        """Step 1: Collect patient symptoms."""
        pass
    
    @abstractmethod
    def examine_patient(self, patient_name: str):
        """Step 2: Physical examination."""
        pass
    
    @abstractmethod
    def perform_tests(self, patient_name: str) -> str:
        """Step 3: Perform tests and get diagnosis."""
        pass
    
    @abstractmethod
    def create_treatment_plan(self, patient_name: str, diagnosis: str) -> str:
        """Step 4: Create treatment plan."""
        pass


class CardiologyDiagnosis(DiagnosisProcess):
    """Concrete - Cardiology diagnosis workflow."""
    
    def collect_symptoms(self, patient_name: str):
        print(f"[Cardiology] Collecting symptoms from {patient_name}")
        print("  → Chest pain? Shortness of breath? Palpitations?")
    
    def examine_patient(self, patient_name: str):
        print(f"[Cardiology] Physical examination of {patient_name}")
        print("  → Checking heart rate and blood pressure")
        print("  → Listening to heart sounds")
    
    def perform_tests(self, patient_name: str) -> str:
        print(f"[Cardiology] Running tests for {patient_name}")
        print("  → EKG performed")
        print("  → Echocardiogram performed")
        print("  → Blood work analyzed")
        return "Mild hypertension detected"
    
    def create_treatment_plan(self, patient_name: str, diagnosis: str) -> str:
        print(f"[Cardiology] Treatment plan for {patient_name}")
        print(f"  Diagnosis: {diagnosis}")
        print("  → Prescribe antihypertensive medication")
        print("  → Recommend lifestyle changes")
        print("  → Schedule follow-up in 4 weeks")
        return "Cardiology treatment plan created"


class DermatologyDiagnosis(DiagnosisProcess):
    """Concrete - Dermatology diagnosis workflow."""
    
    def collect_symptoms(self, patient_name: str):
        print(f"[Dermatology] Collecting symptoms from {patient_name}")
        print("  → Skin condition description? Duration? Itching? Pain?")
    
    def examine_patient(self, patient_name: str):
        print(f"[Dermatology] Physical examination of {patient_name}")
        print("  → Visual inspection of affected area")
        print("  → Checking skin texture and appearance")
    
    def perform_tests(self, patient_name: str) -> str:
        print(f"[Dermatology] Running tests for {patient_name}")
        print("  → Patch test performed")
        print("  → Fungal culture if needed")
        return "Contact dermatitis identified"
    
    def create_treatment_plan(self, patient_name: str, diagnosis: str) -> str:
        print(f"[Dermatology] Treatment plan for {patient_name}")
        print(f"  Diagnosis: {diagnosis}")
        print("  → Prescribe topical steroid cream")
        print("  → Recommend avoiding irritants")
        print("  → Schedule follow-up in 2 weeks")
        return "Dermatology treatment plan created"


class PsychiatryDiagnosis(DiagnosisProcess):
    """Concrete - Psychiatry diagnosis workflow."""
    
    def collect_symptoms(self, patient_name: str):
        print(f"[Psychiatry] Collecting symptoms from {patient_name}")
        print("  → Mood changes? Sleep issues? Anxiety levels?")
    
    def examine_patient(self, patient_name: str):
        print(f"[Psychiatry] Psychological evaluation of {patient_name}")
        print("  → Cognitive assessment")
        print("  → Emotional evaluation")
    
    def perform_tests(self, patient_name: str) -> str:
        print(f"[Psychiatry] Running tests for {patient_name}")
        print("  → Depression scale assessment")
        print("  → Anxiety inventory completed")
        return "Moderate depression with anxiety"
    
    def create_treatment_plan(self, patient_name: str, diagnosis: str) -> str:
        print(f"[Psychiatry] Treatment plan for {patient_name}")
        print(f"  Diagnosis: {diagnosis}")
        print("  → Recommend psychotherapy (CBT)")
        print("  → Consider antidepressant medication")
        print("  → Schedule weekly sessions")
        return "Psychiatry treatment plan created"


# Example usage
if __name__ == "__main__":
    print("=== Template Method Pattern Example: Medical Diagnosis ===\n")
    
    patient_name = "Sarah Johnson"
    
    # Cardiology diagnosis
    print("--- CARDIOLOGY APPOINTMENT ---")
    cardio = CardiologyDiagnosis()
    result = cardio.diagnose_patient(patient_name)
    print(f"Result: {result}\n\n")
    
    # Dermatology diagnosis
    print("--- DERMATOLOGY APPOINTMENT ---")
    derma = DermatologyDiagnosis()
    result = derma.diagnose_patient(patient_name)
    print(f"Result: {result}\n\n")
    
    # Psychiatry diagnosis
    print("--- PSYCHIATRY APPOINTMENT ---")
    psych = PsychiatryDiagnosis()
    result = psych.diagnose_patient(patient_name)
    print(f"Result: {result}\n")
    
    print("=== End of Example ===")

