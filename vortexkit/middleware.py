class Middleware:
    """
    Base class for middleware components that process requests before route handling.

    Methods:
        process_request(request):
            Process the request data before the route handler is called.

            Args:
                request: The request object.
    """

    def process_request(self, request):
        """
        Process the request data before the route handler is called.

        Args:
            request: The request object.
        """
        pass
