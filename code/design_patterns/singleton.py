"""
Singleton Pattern Example

The Singleton pattern ensures a class has only one instance and provides 
a global point of access to it.

This example demonstrates a hospital database connection that should only 
exist once throughout the application.
"""


class Singleton:
    """Base Singleton class - ensures only one instance exists."""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class HospitalDatabase(Singleton):
    """Hospital database connection - only one instance should exist."""
    
    def __init__(self):
        if not hasattr(self, 'connection'):  # Initialize only once
            self.connection = None
            self.is_connected = False
    
    def connect(self, host: str = "localhost", port: int = 5432):
        """Connect to the hospital database."""
        if not self.is_connected:
            self.connection = f"Connected to Hospital DB at {host}:{port}"
            self.is_connected = True
            print(f"✓ {self.connection}")
        else:
            print("✓ Already connected to Hospital DB")
        return self.connection
    
    def disconnect(self):
        """Disconnect from the database."""
        if self.is_connected:
            self.connection = None
            self.is_connected = False
            print("✓ Disconnected from Hospital DB")
    
    def query_patient(self, patient_id: int):
        """Query patient information."""
        if not self.is_connected:
            raise RuntimeError("Database not connected")
        return f"Patient #{patient_id} data retrieved from database"
    
    def query_prescriptions(self, patient_id: int):
        """Query patient prescriptions."""
        if not self.is_connected:
            raise RuntimeError("Database not connected")
        return f"Prescriptions for Patient #{patient_id} retrieved"


# Example usage
if __name__ == "__main__":
    print("=== Singleton Pattern Example: Hospital Database ===\n")
    
    # Create first database reference
    db1 = HospitalDatabase()
    db1.connect()
    print(f"db1 instance id: {id(db1)}\n")
    
    # Try to create another database reference
    db2 = HospitalDatabase()
    print(f"db2 instance id: {id(db2)}\n")
    
    # Verify they are the same instance
    print(f"db1 is db2: {db1 is db2}")
    print(f"Connected: {db2.is_connected}\n")
    
    # Use the database through any reference
    print(db1.query_patient(12345))
    print(db2.query_prescriptions(12345))
    print()
    
    # Disconnect
    db1.disconnect()
    print(f"After disconnect - is_connected: {db2.is_connected}")
    
    print("\n=== End of Example ===")

