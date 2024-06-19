from dataclasses import dataclass, field
import json
import mimetypes

@dataclass
class PlainTextResponse:
    """
        A response that returns plain text content.

        Args:
            content (str): The plain text content to return.
            status_code (str): The status code of the response. Default is '200 OK'.
    """
    content: str
    content_type: str = field(default='text/plain', init=False)
    status_code: str = "200 OK"

@dataclass
class HtmlResponse:
    """
        A response that returns HTML content.
        
        Args:
            content (str): The HTML content to return.
            status_code (str): The status code of the response. Default is '200 OK'.
    """
    content: str
    content_type: str = field(default='text/html; charset=utf-8', init=False)
    status_code: str = "200 OK"

@dataclass
class FileResponse:
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
        in_file = open(self.filePath, "rb")
        data = in_file.read()
        if data == None:
            raise FileNotFoundError("File was not found.") 
        else:
            self.content_type = mimetypes.guess_type(self.filePath)[0]
            self.content = data
    
@dataclass
class JSONResponse:
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
        self.content = json.dumps(self.dictionary)

@dataclass
class RedirectResponse:
    """
        A response that redirects to a different location.

        Args:
            location (str): The location to redirect to.
            status_code (str): The status code of the response. Default is '302 Found'.
            content (str): The content of the response. Default is None.
    """
    location: str
    status_code: str = "302 Found"
    content_type: str = field(default='text/html; charset=utf-8', init=False)
    content: str = field(default=None, init=False)

    def __post_init__(self):
        self.content = f"<html><head><meta http-equiv='refresh' content='0;url={self.location}'></head><body><a href='{self.location}'>Redirecting...</a></body></html>"

@dataclass
class TemplateResponse:
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
        with open(self.file_path) as f:
            file_content = f.read()
            for key, value in self.variables.items():
                file_content = file_content.replace(f"(({key}))", value)
                file_content = file_content.replace(f"(( {key} ))", value)
            self.content = file_content