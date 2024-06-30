import os
import threading
from wsgiref import simple_server
from urllib.parse import parse_qs
from .responses import FileResponse
from .request import ParseRequestInput
from .enums import StatusCode

class App:
    """
    Represents a web application using VortexKit framework.

    Attributes:
        _routes (dict): Dictionary mapping routes to handler functions.
        errors (dict): Dictionary mapping error status codes to handler functions.
        context (threading.local): Thread-local storage for request context.
        middleware (list): List of middleware functions to be applied to requests.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the App class.
        """
        self._routes = {}
        self.errors = {}
        self.context = threading.local()
        self.middleware = []

    def register_middleware(self, middleware: callable) -> None:
        """
        Registers a middleware function to be applied to incoming requests.

        Args:
            middleware (callable): Callable middleware function with a 'process_request' method.
        
        Raises:
            ValueError: If the provided middleware does not have a 'process_request' method.
        """
        if not hasattr(middleware, "process_request"):
            raise ValueError("Middleware must have a 'process_request' method")

        self.middleware.append(middleware)

    def register_class(self, cls: any) -> None:
        """
        Registers a class as a route handler in the application.

        Args:
            cls (any): Class to be registered as a route handler.
        """
        self.add_route("/", cls.__call__)

    def serve_static(self, path: str, folder: str) -> None:
        """
        Serves static files from a specified folder.

        Args:
            path (str): URL path prefix for serving static files.
            folder (str): Local folder path containing static files.
        """
        for file in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, file)):
                self._routes[f"{path}/{file}"] = [lambda file=file: FileResponse(os.path.join(folder, file)), True]

    def websocket(self, path: str) -> callable:
        """
        Decorator to define a WebSocket route.

        Args:
            path (str): URL path for the WebSocket route.

        Returns:
            callable: Decorated function handling the WebSocket route.
        
        Raises:
            ValueError: If the path does not start with '/' or if the route already exists.
        """
        def inner(func, *args, **kwargs):
            if not path.startswith("/") and path != "*":
                raise ValueError("Path must start with a /")
            if self._routes.get(path):
                raise ValueError("Route already exists")
            self._routes[path] = [func]
            return func
        return inner

    def route(self, path: str) -> callable:
        """
        Decorator to define a new HTTP route.

        Args:
            path (str): URL path for the route.

        Returns:
            callable: Decorated function handling the HTTP route.
        
        Raises:
            ValueError: If the path does not start with '/' or if the route already exists.
        """
        def inner(func, *args, **kwargs):
            if not path.startswith("/") and path != "*":
                raise ValueError("Path must start with a /")
            if self._routes.get(path):
                raise ValueError("Route already exists")
            self._routes[path] = [func]
            return func
        return inner

    def error_handler(self, status_code: int|StatusCode) -> callable:
        """
        Decorator to define an error handler for a specific HTTP status code.

        Args:
            status_code (int|StatusCode): HTTP status code or StatusCode enum.

        Returns:
            callable: Decorated function handling the error.
        
        Raises:
            ValueError: If the error handler for the specified status code already exists.
        """
        if isinstance(status_code, StatusCode):
            status_code = status_code.value
        
        if isinstance(status_code, str):
            status_code = status_code.split(" ")[0]

        def inner(func, *args, **kwargs):
            if self.errors.get(status_code):
                raise ValueError("Error handler for this status code already exists")
            self.errors[status_code] = [func]
            return func
        return inner

    def handler(self, environ: dict, start_response: callable) -> list:
        """
        WSGI handler function for processing incoming requests.

        Args:
            environ (dict): WSGI environment dictionary.
            start_response (callable): WSGI start_response function.

        Returns:
            list: Response content as a list of bytes.
        """
        current_request = ParseRequestInput(environ, self.context).parse()
        print(current_request.__dict__())

        # Invoke middleware and pass current request
        for middleware in self.middleware:
            middleware.process_request(current_request)

        route = self._routes.get(current_request.path, False)

        if not route:
            if self._routes.get("*"):
                route = self._routes["*"]
            else:
                route = self.errors.get("404")
                if not route:
                    start_response("404 Not Found", [("Content-type", "text/html")])
                    return [b"<h1>404 Not Found</h1>"]

                try:
                    response = route[0](current_request)
                except TypeError:
                    response = route[0]()
                if isinstance(response.status_code, StatusCode):
                    response.status_code = response.status_code.value

                start_response(response.status_code, [("Content-type", response.content_type)])
                if isinstance(response.content, bytes):
                    return [response.content]
                return [response.content.encode('utf-8')]

        try:
            response = route[0](current_request)
        except TypeError:
            response = route[0]()
        if isinstance(response.status_code, StatusCode):
            response.status_code = response.status_code.value

        start_response(response.status_code, [("Content-type", response.content_type)])
        if isinstance(response.content, bytes):
            return [response.content]
        return [response.content.encode('utf-8')]

    def add_route(self, path: str, func: callable) -> None:
        """
        Adds a new route to the application.

        Args:
            path (str): URL path for the route.
            func (callable): Function to be called when the route is accessed.
        
        Raises:
            ValueError: If the path does not start with '/' or if the route already exists.
        """
        if not path.startswith("/"):
            raise ValueError("Path must start with a /")
        if self._routes.get(path):
            raise ValueError("Route already exists")

        self._routes[path] = [func]

    def add_error_handler(self, status_code: str|StatusCode, func: callable) -> None:
        """
        Adds a new error handler for a specific HTTP status code.

        Args:
            status_code (str|StatusCode): HTTP status code or StatusCode enum.
            func (callable): Function to be called when the error occurs.
        
        Raises:
            ValueError: If the error handler for the specified status code already exists.
        """
        if isinstance(status_code, StatusCode):
            status_code = status_code.value
        
        if isinstance(status_code, str):
            status_code = status_code.split(" ")[0]

        if not self.errors.get(status_code):
            self.errors[status_code] = [func]

    def run(self, host: str, port: int) -> None:
        """
        Runs the VortexKit application on the specified host and port.

        Args:
            host (str): Host address to run the application on.
            port (int): Port number to run the application on.
        
        Raises:
            ValueError: If no host or port is specified.
        """
        if not host and not port:
            raise ValueError("No host and port were specified.")
        if not host:
            raise ValueError("No host was specified.")
        if not port:
            raise ValueError("No port was specified.")

        assert self._routes.get("/") is not None, "Cannot find index route"
        with simple_server.make_server(host, port, self.handler) as server:
            print(f"[+] Development server running on http://{host}:{port}")
            server.serve_forever()
