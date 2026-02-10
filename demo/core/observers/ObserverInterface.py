class ObserverInterface():
    def __init__(self):
        self.observers = []
    
    
    def attach(self, observer):
        self.observers.append(observer)

    
    def detach(self, observer):
        self.observers.remove(observer)

    
    def notify(self):
        for observer in self.observers:
            observer.update(self)
    
    def update(self, subject):
        raise NotImplementedError