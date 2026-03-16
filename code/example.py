class Observer:
    def update(self, patient, *args, **kwargs):
        raise NotImplementedError


class Patient:
    def __init__(self, observer, _id):
        self.observer = observer
        self.id = _id
        self.illness = False
        self.days_ill = 0
        self.interactions = []

    def falls_ill(self):
        self.illness = True

    def recovers(self):
        self.illness = False
        self.days_ill = 0

    def notify(self, *args, **kwargs):
        self.observer.update(self, *args, **kwargs)


patients = [Patient(Observer(), i) for i in range(1000)]
