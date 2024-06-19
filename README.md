# 🌪️ WhirlWind

WhirlWind is a lightweight, customizable WSGI framework designed to handle web requests with ease and flexibility. It's perfect for building web applications quickly and efficiently. 🚀

## 🌟 Features

- ⚡ **Lightweight**: Minimal overhead, lightning-fast performance.
- 🛠️ **Customizable**: Easily extend and modify to fit your needs.
- 📦 **Built-in Tools**: Includes request parsing, routing, and more.
- 🧪 **Test-Friendly**: Designed with testing in mind.

## 🚀 Getting Started

### 📦 Installation

Install WhirlWind via pip:

```bash
pip install whirl_wind
```

### 🔧 Usage

Create a simple application with WhirlWind:

```python
from WhirlWind import App, PlainTextResponse, Request

app = App()

@app.route("/")
def home(req: Request):
    return PlainTextResponse(f"Hello, World! Your requesting from {req.path}!")

if __name__ == "__main__":
    app.run("localhost", 8080)
```

Run your application:

```bash
python app.py
```

### 🛠️ Advanced Usage

#### Handling Different Content Types

WhirlWind can handle various content types including JSON, XML, and multipart form data.

```python
from WhirlWind import App, JSONResponse, Request

app = App()

@app.route('/upload', methods=['POST'])
def upload(req: Request):
    if req.content_type.startswith('multipart/form-data'):
        file_data = req.body.get('file')
        return JSONResponse({"filename": file_data.filename, "content": file_data.file.read().decode()})
    return JSONResponse({"error": "Unsupported Content Type"}, status_code="400 Bad Request")

if __name__ == "__main__":
    app.run("localhost", 8080)
```

### 📖 Documentation

For detailed documentation, visit the [WhirlWind Docs](https://github.com/daftscientist/whirlwind/wiki).

## 💻 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](https://github.com/daftscientist/whirlwind/blob/main/CONTRIBUTING.md) for details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/daftscientist/whirlwind/blob/main/LICENSE) file for details.

## 🎉 Acknowledgements

Thanks to all contributors and supporters of WhirlWind. Your efforts make this project better every day. 🌟