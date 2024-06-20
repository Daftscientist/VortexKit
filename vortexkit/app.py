import os
from wsgiref import simple_server
from urllib.parse import parse_qs
from .responses import FileResponse
from .request import ParseRequestInput

class App(object):
    """
        The initial class that is used to create a new vortexkit app.
    """
    def __init__(self) -> None:
        self._routes = dict()
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
            if not path.startswith("/"):
                raise ValueError("Path must start with a /")
            if self._routes.get(path):
                raise ValueError("Route already exists")
            self._routes[path] = [func]
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
        if route:
            try:
                response = route[0](current_request)
            except TypeError:
                response = route[0]()
            start_response(response.status_code, [("Content-type", response.content_type)])
            return [response.content.encode('utf-8')]
        else:
            start_response("404 Not Found", [("Content-type", "text/html")])
            return [b"<h1>404 Not Found</h1>"]


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