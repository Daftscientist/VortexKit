import vortexkit

app = vortexkit.App()

class TestMiddleware(vortexkit.Middleware):
    def process_request(self, request: vortexkit.Request):
        print("Middleware processed request from route:", request.path)

app.register_middleware(TestMiddleware())

@app.route("/")
def home(request: vortexkit.Request):
    return vortexkit.PlainTextResponse("Hello, World!")

if __name__ == '__main__':
    app.run(
        host="localhost",
        port=8000,
    )