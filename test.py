from vortexkit import App, Request, JSONResponse, StatusCode, TemplateResponse, FileResponse

app = App()

@app.route("/")
def index(request: Request):
    return JSONResponse({"message": "Hello, world!"})

@app.route("/test")
def test(request: Request):
    return FileResponse("template.html")

@app.error_handler(StatusCode.NOT_FOUND)
def other(request: Request):
    return JSONResponse({"message": "This route is a not found"}, StatusCode.NOT_FOUND)

if __name__ == '__main__':
    app.run(
        host="localhost",
        port=8000,
    )