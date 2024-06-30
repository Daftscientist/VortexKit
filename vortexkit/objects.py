class Route:
    """
    Represents a route in the VortexKit object model.

    Attributes:
        path (str): The path of the route.
        handler (callable): The callable object that handles requests to this route.
    """

    def __init__(self, path: str, handler: callable) -> None:
        """
        Initialize a Route object.

        Args:
            path (str): The path of the route.
            handler (callable): The callable object that handles requests to this route.
        """
        self.path = path
        self.handler = handler
    
    def __call__(self, *args, **kwargs):
        """
        Call the handler callable with the provided arguments.

        Returns:
            The result of calling the handler.
        """
        return self.handler(*args, **kwargs)
