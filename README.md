
# WhirlWind

WhirlWind is a lightweight Python web framework for building web applications quickly and efficiently.

## Installation

You can install WhirlWind using pip:

```
pip install https://github.com/Daftscientist/WhirlWind.git
```

## Usage

```python
from WhirlWind import App, responses

# Initial app setup
app = App(staticFolder="static")

# Define routes
@app.path('/')
def index():
    return responses.TemplateResponse("index.html", variables={"hello": "hi"})

@app.path('/html')
def html():
    return responses.HtmlResponse("<a href='/'>Link Back To Home</a>")

@app.path('/plain-text')
def plainText():
    return responses.PlainTextResponse("Hello <a href='/'>Link Back To Home</a> lmao")

@app.path('/file')
def file():
    return responses.FileResponse("test.json")

# Run the webserver
if __name__ == "__main__":
    app.run("localhost", 5000)
```

## Features

- **Routing:** Easily define routes for different URL endpoints.
- **Response Types:** Supports various response types including HTML, plain text, and file responses.
- **Static Files:** Serve static files effortlessly with the specified static folder.
- **Lightweight:** Minimalistic design for quick setup and performance.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
