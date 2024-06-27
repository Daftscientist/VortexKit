import vortexkit

app = vortexkit.App()

app.context.application_name = "My App"

class TestMiddleware(vortexkit.Middleware):
    def process_request(self, request: vortexkit.Request):
        request.context.name = "added by middleware"

        print("Middleware processed request from route:", request.path)

app.register_middleware(TestMiddleware())

@app.route("/")
def home(request: vortexkit.Request):
    print(request.app.context.application_name)
    return vortexkit.PlainTextResponse("Hello, World!, " + request.context.name)

if __name__ == '__main__':
    app.run(
        host="localhost",
        port=8000,
    )