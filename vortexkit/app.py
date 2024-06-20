import os
from wsgiref import simple_server
from urllib.parse import parse_qs
from .responses import FileResponse
from .request import ParseRequestInput
from .enums import StatusCode

class App(object):
    """
        The initial class that is used to create a new vortexkit app.
    """
    def __init__(self) -> None:
        self._routes = dict()
        self.errors = dict()
        """
            {
                "/": [function, content_type],
            }
        """
    
    def serve_static(self, path: str, folder: str) -> None:
        """
            Serves static files from a specified folder.

            Args:
                path (str): The path to serve the static files from.
                folder (str): The folder to serve the static files from.
        """
        for file in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, file)):
                self._routes[f"{path}/{file}"] = [lambda file=file: FileResponse(os.path.join(folder, file)), True]

    def route(self, path: str) -> None:
        """
            A decorator that creates a new route.

            Args:
                path (str): The path of the route.
        """

        def inner(func, *args, **kwargs):
            if not path.startswith("/") and not path == "*":
                raise ValueError("Path must start with a /")
            if self._routes.get(path):
                raise ValueError("Route already exists")
            self._routes[path] = [func]
            return func
        return inner

    def error_handler(self, status_code: int|StatusCode) -> None:
        """
            A decorator that creates a new route.

            Args:
                path (str): The path of the route.
        """

        if type(status_code) is StatusCode:
            status_code = status_code.value
        
        if type(status_code) is str:
            status_code = status_code.split(" ")[0]

        def inner(func, *args, **kwargs):
            if self.errors.get(status_code):
                raise ValueError("Route already exists")
            self.errors[status_code] = [func]
            return func
        return inner

    def handler(self, environ: dict, start_response: callable) -> list:
        """
        The WSGI handler for the app.

        Args:
            environ (dict): The WSGI environ.
            start_response (callable): The WSGI start_response.
        """
    
        current_request = ParseRequestInput(environ).parse()
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
                if type(response.status_code) is StatusCode:
                    response.status_code = response.status_code.value
                
                start_response(response.status_code, [("Content-type", response.content_type)])
                return [response.content.encode('utf-8')]
        
        try:
            response = route[0](current_request)
        except TypeError:
            response = route[0]()
        if type(response.status_code) is StatusCode:
            response.status_code = response.status_code.value
        
        start_response(response.status_code, [("Content-type", response.content_type)])
        return [response.content.encode('utf-8')]

    def add_route(self, path: str, func: callable) -> None:
        """
            Adds a new route to the app.

            Args:
                path (str): The path of the route.
                func (callable): The function to be called when the route is accessed.
        """
        if not path.startswith("/"):
            raise ValueError("Path must start with a /")
        if self._routes.get(path):
            raise ValueError("Route already exists")

        self._routes[path] = [func]
    
    def add_error_handler(self, status_code: str|StatusCode, func: callable) -> None:
        """
            Adds a new error handler to the app.

            Args:
                status_code (str): The status code of the error.
                func (callable): The function to be called when the error occurs.
        """

        if type(status_code) is StatusCode:
            status_code = status_code.value
        
        if type(status_code) is str:
            status_code = status_code.split(" ")[0]

        if not self.errors.get(status_code):
            self.errors[status_code] = [func]

    def run(self, host: str, port: int) -> None:
        """
            Runs the vortexkit app on the specified host and port.

            Args:
                host (str): The host to run the app on.
                port (int): The port to run the app on.
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