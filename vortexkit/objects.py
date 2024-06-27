## derivertive classes for the VortexKit object model

## derivetive class for route
class Route:
    def __init__(self, path: str, handler: callable) -> None:
        self.path = path
        self.handler = handler
    
    def __call__(self, *args, **kwargs):
        return self.handler(*args, **kwargs)