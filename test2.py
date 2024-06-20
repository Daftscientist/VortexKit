import threading


class App(object):
    """
        The initial class that is used to create a new vortexkit app.
    """
    def __init__(self) -> None:
        self._routes = dict()
        self.errors = dict()
        self.context = threading.local()

myapp = App()

myapp.context.name = "My App"

print(myapp.context.__dict__)