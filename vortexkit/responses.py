from dataclasses import dataclass, field
import json
import mimetypes
from http.cookies import SimpleCookie

from dataclasses import dataclass, field
import json
import mimetypes
from http.cookies import SimpleCookie

class BaseResponse:
    """
    Base class for all response types, providing common functionality like cookie and header handling.
    """
    cookies: SimpleCookie = None
    headers: dict = None

    def __init__(self):
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

        Args:
            content (str): The plain text content to return.
            status_code (str): The status code of the response. Default is '200 OK'.
    """
    content: str
    content_type: str = field(default='text/plain', init=False)
    status_code: str = "200 OK"

    def __post_init__(self):
        super().__init__()  # Initialize BaseResponse

@dataclass
class HtmlResponse(BaseResponse):
    """
        A response that returns HTML content.
        
        Args:
            content (str): The HTML content to return.
            status_code (str): The status code of the response. Default is '200 OK'.
    """
    content: str
    content_type: str = field(default='text/html; charset=utf-8', init=False)
    status_code: str = "200 OK"

    def __post_init__(self):
        super().__init__()

@dataclass
class FileResponse(BaseResponse):
    """
        A response that returns a file.

        Args:
            file_path (str): The path to the file to return.
            status_code (str): The status code of the response. Default is '200 OK'.
    """
    file_path: str
    content_type: str = field(default=None, init=False)
    status_code: str = "200 OK"
    content: bytes = field(default=None, init=False)

    def __post_init__(self):
        super().__init__()  # Initialize BaseResponse

        in_file = open(self.filePath, "rb")
        data = in_file.read()
        if data == None:
            raise FileNotFoundError("File was not found.") 
        else:
            self.content_type = mimetypes.guess_type(self.filePath)[0]
            self.content = data
    
@dataclass
class JSONResponse(BaseResponse):
    """
        A response that returns a JSON object.

        Args:
            dictionary (dict): The dictionary to be converted to JSON.
            status_code (str): The status code of the response. Default is '200 OK'.
    """
    dictionary: dict
    content_type: str = field(default='application/json', init=False)
    status_code: str = "200 OK"
    content: str = field(default=None, init=False)

    def __post_init__(self):
        super().__init__()  # Initialize BaseResponse

        self.content = json.dumps(self.dictionary)

@dataclass
class RedirectResponse(BaseResponse):
    """
    A response that redirects to a different location.

    Args:
        location (str): The location to redirect to.
    """
    location: str
    status_code: str = field(default='302 Found', init=False)
    content_type: str = field(default='text/html; charset=utf-8', init=False)
    content: str = field(default=None, init=False)

    def __post_init__(self):
        super().__init__()  # Initialize BaseResponse
        self.add_header('Location', self.location)
        self.content = f"<html><head><meta http-equiv='refresh' content='0;url={self.location}'></head><body>If you are not redirected, <a href='{self.location}'>click here</a>.</body></html>"

@dataclass
class TemplateResponse(BaseResponse):
    """
        A response that renders a template file with the given variables.

        Args:
            file_path (str): The path to the template file.
            variables (dict): A dictionary of variables to replace in the template file.
            status_code (str): The status code of the response. Default is '200 OK'.
    """
    file_path: str
    variables: dict
    content_type: str = field(default='text/html; charset=utf-8', init=False)
    status_code: str = "200 OK"
    content: str = field(default=None, init=False)

    def __post_init__(self):
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

        Args:
            file_path (str): The path to the file to stream.
            chunk_size (int): The size of each chunk to stream. Default is 1024.
            status_code (str): The status code of the response. Default is '200 OK'.
    """
    file_path: str
    chunk_size: int = 1024
    content_type: str = field(default=None, init=False)
    status_code: str = "200 OK"
    content: bytes = field(default=None, init=False)

    def __post_init__(self):
        super().__init__()
        self.content_type = mimetypes.guess_type(self.file_path)[0]

    def __iter__(self):
        with open(self.file_path, "rb") as f:
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break
                yield chunk