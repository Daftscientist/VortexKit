import functools
import typing
import os
import mimetypes
from wsgiref import simple_server, util

class TerminalEffects:
    FINE = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class App(object):
    def __init__(self, staticFolder, secretKey=None):
        self.secretKey = str(secretKey)
        self._routes = dict()
        self.staticFolder = str(staticFolder)

    def run(self, host=None, port=None):
        if not host and not port:
            print(terminalEffects.FAIL + '[-] No host and port were spesified.' + terminalEffects.ENDC)
            exit()
        if not host:
            print(terminalEffects.FAIL + '[-] No host was specified.' + terminalEffects.ENDC)
            exit()
        if not port:
            print(terminalEffects.FAIL + '[-] No port was specified.' + terminalEffects.ENDC)
            exit()

        assert self._routes.get("/") is not None, "Cannot find index route"

        with simple_server.make_server(host, port, self.appHandler) as server:
            print(terminalEffects.FINE + '[+] Development server running on http://' + host + ':' + str(port) + terminalEffects.ENDC)
            server.serve_forever()


    def path(self, path: str) -> None:
        route = path.lower()

        if not route.startswith('/'):
            raise ValueError('Route must start with a slash')
        if self._routes.get(route, False):
            raise ValueError('This route already exists')

        def inner(func):
            self._routes.update({ route: [ func()[0], func()[1] ] })
            return func
        return inner

    def appHandler(self, environ, respond):
        fn = environ["PATH_INFO"]

        routeExists = self._routes.get(fn)

        if routeExists:
            headers = [('Content-type', routeExists[1])]  # HTTP Headers
            status = '200 OK'  # HTTP Status
            respond(status, headers)
            stuff = routeExists[0]
            return [stuff] # returns the content to show on the path from the func

        respond('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'not found'] # returns the content on the path if it is 404
