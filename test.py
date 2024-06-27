from vortexkit import App, Request, JSONResponse, StatusCode, Middleware, FileResponse

app = App()

class TestMiddleware(Middleware):
    def process_request(self, request: Request):
        request.context.name = "added by middleware"

        print("Middleware processed request from route:", request.path)

app.register_middleware(TestMiddleware())

app.context.name = "My App"

@app.route("/")
def home(request: Request):
    if not request.method == "POST":
        return JSONResponse({"message": "This route only accepts POST requests"}, StatusCode.BAD_REQUEST)
    
    params = request.body

    if not params['data']:
        return JSONResponse({"message": "No data was provided"}, StatusCode.BAD_REQUEST)
    
    request.context.data = params['data']

    return JSONResponse({"data": request.context.__dict__})

@app.error_handler(StatusCode.NOT_FOUND)
def other(request: Request):
    return JSONResponse({"message": "This route is a not found"}, StatusCode.NOT_FOUND)

if __name__ == '__main__':
    app.run(
        host="localhost",
        port=8000,
    )