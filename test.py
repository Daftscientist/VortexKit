from vortexkit import App, Request, JSONResponse, StatusCode, Middleware, FileResponse

app = App()

class TestMiddleware(Middleware):
    def process_request(self, request: Request):
        print("Middleware processed request from route:", request.path)

app.register_middleware(TestMiddleware())

app.context.name = "My App"

@app.route("/")
def index(request: Request):
    print(request)
    return JSONResponse({"message": "Hello, world!", "app_name": request.app.context.name})

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