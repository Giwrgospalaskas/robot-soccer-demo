class ObserverInterface():
    def __init__(self):
        self.observers = []
    
    
    def attach(self, observer):
        try:
            self.observers.append(observer)
            print(f"attached {type(observer).__name__}")
        except Exception as e:
            print(f"Error attaching {type(observer).__name__}: {e}")
            
    
    def detach(self, observer):
        try:
            self.observers.remove(observer)
            print(f"detached {type(observer).__name__}")
        except Exception as e:
            print(f"Error detaching {type(observer).__name__}: {e}")

    
    def notify(self, state):
        for observer in self.observers:
            observer.update(state)
    
    def update(self, state):
        raise NotImplementedError