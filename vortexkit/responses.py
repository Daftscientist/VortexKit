from dataclasses import dataclass, field
import json
import mimetypes
from http.cookies import SimpleCookie

class BaseResponse:
    """
    Base class for all response types, providing common functionality like cookie and header handling.

    Attributes:
        cookies (SimpleCookie): An instance of SimpleCookie for managing cookies.
        headers (dict): A dictionary for managing HTTP headers.

    Methods:
        set_cookie(key, value, **kwargs):
            Sets a cookie with the given key, value, and optional attributes.
        
        remove_cookie(key, path='/', domain=None):
            Removes a cookie by setting its expiry date in the past.

        add_header(key, value):
            Adds or updates an HTTP header with the given key-value pair.

        remove_header(key):
            Removes an HTTP header if it exists.

        get_header(key):
            Retrieves the value of an HTTP header if it exists.
    """

    cookies: SimpleCookie = None
    headers: dict = None

    def __init__(self):
        """
        Initializes the BaseResponse with empty cookies and headers.
        """
        self.cookies = SimpleCookie()
        self.headers = {}

    def set_cookie(self, key, value, **kwargs):
        """
        Sets a cookie.

        Args:
            key (str): The name of the cookie.
            value (str): The value of the cookie.
            kwargs: Additional cookie attributes, e.g., expires, path, domain.
        """
        self.cookies[key] = value
        for attr, attr_value in kwargs.items():
            self.cookies[key][attr] = attr_value
    
    def remove_cookie(self, key, path='/', domain=None):
        """
        Removes a cookie by setting its expiry date in the past.

        Args:
            key (str): The name of the cookie to remove.
            path (str, optional): The path from which the cookie will be removed. Defaults to '/'.
            domain (str, optional): The domain from which the cookie will be removed. If not specified, the cookie will only be removed from the domain of the current request.
        """
        if key in self.cookies:
            self.cookies[key] = ''
            self.cookies[key]['path'] = path
            if domain:
                self.cookies[key]['domain'] = domain
            self.cookies[key]['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'

    def add_header(self, key, value):
        """
        Adds or updates a header.

        Args:
            key (str): The name of the header.
            value (str): The value of the header.
        """
        self.headers[key] = value

    def remove_header(self, key):
        """
        Removes a header if it exists.

        Args:
            key (str): The name of the header to remove.
        """
        if key in self.headers:
            del self.headers[key]

    def get_header(self, key):
        """
        Gets the value of a header.

        Args:
            key (str): The name of the header.

        Returns:
            The value of the header if it exists, None otherwise.
        """
        return self.headers.get(key)

@dataclass
class PlainTextResponse(BaseResponse):
    """
    A response that returns plain text content.

    Attributes:
        content (str): The plain text content to return.
        content_type (str): The content type of the response ('text/plain').
        status_code (str): The status code of the response. Default is '200 OK'.

    Methods:
        __post_init__():
            Initializes the PlainTextResponse and sets the content type.
    """

    content: str
    content_type: str = field(default='text/plain', init=False)
    status_code: str = "200 OK"

    def __post_init__(self):
        """
        Initializes the PlainTextResponse and sets the content type.
        """
        super().__init__()  # Initialize BaseResponse

@dataclass
class HtmlResponse(BaseResponse):
    """
    A response that returns HTML content.
    
    Attributes:
        content (str): The HTML content to return.
        content_type (str): The content type of the response ('text/html; charset=utf-8').
        status_code (str): The status code of the response. Default is '200 OK'.

    Methods:
        __post_init__():
            Initializes the HtmlResponse and sets the content type.
    """

    content: str
    content_type: str = field(default='text/html; charset=utf-8', init=False)
    status_code: str = "200 OK"

    def __post_init__(self):
        """
        Initializes the HtmlResponse and sets the content type.
        """
        super().__init__()

@dataclass
class FileResponse(BaseResponse):
    """
    A response that returns a file.

    Attributes:
        file_path (str): The path to the file to return.
        content_type (str): The detected content type of the file.
        status_code (str): The status code of the response. Default is '200 OK'.
        content (bytes): The content of the file as bytes.

    Methods:
        __post_init__():
            Initializes the FileResponse and reads the file content.
    """

    file_path: str
    content_type: str = field(default=None, init=False)
    status_code: str = "200 OK"
    content: bytes = field(default=None, init=False)

    def __post_init__(self):
        """
        Initializes the FileResponse and reads the file content.
        Raises:
            FileNotFoundError: If the file is not found.
        """
        super().__init__()  # Initialize BaseResponse

        try:
            with open(self.file_path, "rb") as in_file:
                self.content = in_file.read()
                if self.content:
                    self.content_type = mimetypes.guess_type(self.file_path)[0]
                else:
                    raise FileNotFoundError("File was found, but no data was returned.") 
        except FileNotFoundError:
            raise FileNotFoundError("File was not found.") 

@dataclass
class JSONResponse(BaseResponse):
    """
    A response that returns a JSON object.

    Attributes:
        dictionary (dict): The dictionary to be converted to JSON.
        content_type (str): The content type of the response ('application/json').
        status_code (str): The status code of the response. Default is '200 OK'.
        content (str): The JSON content as a string.

    Methods:
        __post_init__():
            Initializes the JSONResponse and converts the dictionary to JSON.
    """

    dictionary: dict
    content_type: str = field(default='application/json', init=False)
    status_code: str = "200 OK"
    content: str = field(default=None, init=False)

    def __post_init__(self):
        """
        Initializes the JSONResponse and converts the dictionary to JSON.
        """
        super().__init__()  # Initialize BaseResponse

        self.content = json.dumps(self.dictionary)

@dataclass
class RedirectResponse(BaseResponse):
    """
    A response that redirects to a different location.

    Attributes:
        location (str): The location to redirect to.
        status_code (str): The status code of the response ('302 Found').
        content_type (str): The content type of the response ('text/html; charset=utf-8').
        content (str): The HTML content for redirection.

    Methods:
        __post_init__():
            Initializes the RedirectResponse and adds the 'Location' header.
    """

    location: str
    status_code: str = field(default='302 Found', init=False)
    content_type: str = field(default='text/html; charset=utf-8', init=False)
    content: str = field(default=None, init=False)

    def __post_init__(self):
        """
        Initializes the RedirectResponse and adds the 'Location' header.
        """
        super().__init__()  # Initialize BaseResponse
        self.add_header('Location', self.location)
        self.content = f"<html><head><meta http-equiv='refresh' content='0;url={self.location}'></head><body>If you are not redirected, <a href='{self.location}'>click here</a>.</body></html>"

@dataclass
class TemplateResponse(BaseResponse):
    """
    A response that renders a template file with the given variables.

    Attributes:
        file_path (str): The path to the template file.
        variables (dict): A dictionary of variables to replace in the template file.
        content_type (str): The content type of the response ('text/html; charset=utf-8').
        status_code (str): The status code of the response. Default is '200 OK'.
        content (str): The rendered template content as a string.

    Methods:
        __post_init__():
            Initializes the TemplateResponse and replaces variables in the template file.
    """

    file_path: str
    variables: dict
    content_type: str = field(default='text/html; charset=utf-8', init=False)
    status_code: str = "200 OK"
    content: str = field(default=None, init=False)

    def __post_init__(self):
        """
        Initializes the TemplateResponse and replaces variables in the template file.
        """
        super().__init__()  # Initialize BaseResponse

        with open(self.file_path) as f:
            file_content = f.read()
            for key, value in self.variables.items():
                file_content = file_content.replace(f"(({key}))", value)
                file_content = file_content.replace(f"(( {key} ))", value)
            self.content = file_content

@dataclass
class FileStreamResponse(BaseResponse):
    """
    A response that streams a file.

    Attributes:
        file_path (str): The path to the file to stream.
        chunk_size (int): The size of each chunk to stream. Default is 1024.
        content_type (str): The content type of the response.
        status_code (str): The status code of the response. Default is '200 OK'.
        content (bytes): The content of the file as bytes.

    Methods:
        __post_init__():
            Initializes the FileStreamResponse and sets the content type.
        
        __iter__():
            Iterates over the file in chunks and yields each chunk.
    """

    file_path: str
    chunk_size: int = 1024
    content_type: str = field(default=None, init=False)
    status_code: str = "200 OK"
    content: bytes = field(default=None, init=False)

    def __post_init__(self):
        """
        Initializes the FileStreamResponse and sets the content type.
        """
        super().__init__()
        self.content_type = mimetypes.guess_type(self.file_path)[0]

    def __iter__(self):
        """
        Iterates over the file in chunks and yields each chunk.
        """
        with open(self.file_path, "rb") as f:
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break
                yield chunk
