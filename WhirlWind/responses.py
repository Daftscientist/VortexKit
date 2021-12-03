import os
import mimetypes
from pathlib import Path

def TemplateResponse(filePath: str, variables: dict):
    with open(filePath) as f:
        fileContent = Path(filePath).read_text()
    for key in variables:
        fileContent = fileContent.replace(f"(({key}))", variables[key])
        fileContent = fileContent.replace(f"(( {key} ))", variables[key])
    return [fileContent.encode(), 'text/html; charset=utf-8']

def HtmlResponse(content: str):
    return [content.encode(), 'text/html; charset=utf-8']
    
def PlainTextResponse(content: str):
    return [content.encode(), 'text/plain']

def FileResponse(filePath: str):
    in_file = open(filePath, "rb")
    data = in_file.read()
    if data == None:
        raise FileNotFoundError("File was not found.") 
    else:
        return [data, f"{mimetypes.guess_type(filePath)[0]}"]
