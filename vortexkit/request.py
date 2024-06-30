from dataclasses import dataclass
import json
import threading
from urllib.parse import parse_qs
import cgi
import xml.etree.ElementTree as ET
from io import BytesIO

@dataclass
class App:
    """
    Represents the application context for handling requests.

    Attributes:
        context (any): The context object associated with the application.
    """

    context: any

    def __json__(self):
        """
        Convert the App object to a JSON-compatible dictionary.

        Returns:
            dict: A dictionary representation of the App object's context.
        """
        return {
            "context": self.context.__dict__
        }

@dataclass
class Request:
    """
    Represents an HTTP request.

    Attributes:
        app (App): The App object associated with the request.
        path (str): The path of the request.
        method (str): The HTTP method of the request.
        query_params (dict): The query parameters of the request.
        body (any, optional): The body content of the request.
        content_type (str, optional): The content type of the request body.
        headers (str, optional): The headers of the request.
        cookies (dict, optional): The cookies sent with the request.
        real_ip (str, optional): The real IP address of the client.
        user_agent (str, optional): The user agent string of the client.
        accept (str, optional): The accept header of the request.
        remote_host (str, optional): The remote host of the client.
        remote_addr (str, optional): The remote address of the client.
        remote_port (int, optional): The remote port of the client.
        server_name (str, optional): The server name handling the request.
        server_port (int, optional): The server port handling the request.
        server_protocol (str, optional): The server protocol handling the request.
        server_software (str, optional): The server software handling the request.
    """

    app: App
    path: str
    method: str
    query_params: dict
    body: any = None
    content_type: str = None
    headers: str = None
    cookies: dict = None
    real_ip: str = None
    user_agent: str = None
    accept: str = None
    remote_host: str = None
    remote_addr: str = None
    remote_port: int = None
    server_name: str = None
    server_port: int = None
    server_protocol: str = None
    server_software: str = None

    context = threading.local()

    def __dict__(self):
        """
        Convert the Request object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the Request object.
        """
        return {
            "app": self.app.__json__(),
            "path": self.path,
            "method": self.method,
            "query_params": self.query_params,
            "body": self.body,
            "content_type": self.content_type,
            "headers": self.headers,
            "cookies": self.cookies,
            "real_ip": self.real_ip,
            "user_agent": self.user_agent,
            "accept": self.accept,
            "remote_host": self.remote_host,
            "remote_addr": self.remote_addr,
            "remote_port": self.remote_port,
            "server_name": self.server_name,
            "server_port": self.server_port,
            "server_protocol": self.server_protocol,
            "server_software": self.server_software,
            "context": self.context.__dict__
        }

    def __repr__(self):
        """
        Return a string representation of the Request object.

        Returns:
            str: A string representation of the Request object.
        """
        return f"Request(path={self.path}, method={self.method}, query_params={self.query_params}, body={self.body}, content_type={self.content_type}, headers={self.headers}, cookies={self.cookies}, real_ip={self.real_ip}, user_agent={self.user_agent}, accept={self.accept}, remote_host={self.remote_host}, remote_addr={self.remote_addr}, remote_port={self.remote_port}, server_name={self.server_name}, server_port={self.server_port}, server_protocol={self.server_protocol}, server_software={self.server_software})"

class ParseRequestInput:
    """
    Parses the WSGI environment data into a Request object.

    Attributes:
        environ_data (dict): The WSGI environment data containing request information.
        context: The context object associated with the request parsing.

    Methods:
        _fetch_body():
            Fetches and returns the request body from the WSGI environment.

        _parse_cookies(cookies_string):
            Parses and returns cookies from the provided cookies string.

        _parse_body(body):
            Parses and returns the request body based on the content type.

        parse():
            Parses the WSGI environment data into a Request object.

            Returns:
                Request: The parsed Request object.
    """

    def __init__(self, environ_data: dict, context):
        """
        Initialize ParseRequestInput with WSGI environment data and context.

        Args:
            environ_data (dict): The WSGI environment data containing request information.
            context: The context object associated with the request parsing.
        """
        self.environ_data = environ_data
        self.context = context

    def _fetch_body(self):
        """
        Fetches and returns the request body from the WSGI environment.

        Returns:
            bytes: The request body as bytes.
        """
        content_length_str = self.environ_data.get('CONTENT_LENGTH', '0')
        try:
            content_length = int(content_length_str) if content_length_str else 0
        except ValueError:
            content_length = 0

        if content_length > 0:
            body = self.environ_data['wsgi.input'].read(content_length)
        else:
            body = b""
        return body

    def _parse_cookies(self, cookies_string: str):
        """
        Parses cookies from the provided cookies string.

        Args:
            cookies_string (str): The string containing cookies.

        Returns:
            dict: A dictionary of parsed cookies.
        """
        if not cookies_string:
            return {}
        cookies = {}
        if cookies_string:
            for cookie in cookies_string.split(";"):
                key, value = cookie.strip().split("=", 1)
                cookies[key] = value
        return cookies

    def _parse_body(self, body: bytes):
        """
        Parses and returns the request body based on the content type.

        Args:
            body (bytes): The request body as bytes.

        Returns:
            any: The parsed request body.
        """
        content_type = self.environ_data.get('CONTENT_TYPE', '')
        if 'application/json' in content_type:
            try:
                return json.loads(body.decode('utf-8'))
            except json.JSONDecodeError:
                return None
        elif 'application/xml' in content_type or 'text/xml' in content_type:
            return body.decode('utf-8')
        elif 'multipart/form-data' in content_type:
            fp = BytesIO(body)
            env = {'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': content_type}
            form = cgi.FieldStorage(fp=fp, environ=env, keep_blank_values=True)
            return {key: form[key].value for key in form.keys()}
        elif 'application/x-www-form-urlencoded' in content_type:
            return parse_qs(body.decode('utf-8'))
        else:
            return body.decode('utf-8')  # Default case: plain text

    def parse(self):
        """
        Parses the WSGI environment data into a Request object.

        Returns:
            Request: The parsed Request object.
        """
        body = self._fetch_body()
        parsed_body = self._parse_body(body)

        current_request = Request(
            app=App(self.context),
            path=self.environ_data.get("PATH_INFO"),
            method=self.environ_data.get("REQUEST_METHOD"),
            query_params=parse_qs(self.environ_data.get("QUERY_STRING", "")),
            body=parsed_body,
            content_type=self.environ_data.get("CONTENT_TYPE").split("boundary=")[0] if self.environ_data.get("CONTENT_TYPE") else None,
            headers=self.environ_data.get("HTTP_USER_AGENT"),
            cookies=self._parse_cookies(self.environ_data.get("HTTP_COOKIE")),
            real_ip=self.environ_data.get("REMOTE_ADDR"),
            user_agent=self.environ_data.get("HTTP_USER_AGENT"),
            accept=self.environ_data.get("HTTP_ACCEPT"),
            remote_host=self.environ_data.get("REMOTE_HOST"),
            remote_addr=self.environ_data.get("REMOTE_ADDR"),
            remote_port=self.environ_data.get("REMOTE_PORT"),
            server_name=self.environ_data.get("SERVER_NAME"),
            server_port=self.environ_data.get("SERVER_PORT"),
            server_protocol=self.environ_data.get("SERVER_PROTOCOL"),
            server_software=self.environ_data.get("SERVER_SOFTWARE")
        )
        return current_request
