import vortexkit

app = vortexkit.App()

@app.route("/")
def home(request: vortexkit.Request):
    return vortexkit.PlainTextResponse("Hello, World!")

@app.error_handler(vortexkit.StatusCode.NOT_FOUND) # Custom error handler for 404
def not_found(request: vortexkit.Request):
    return vortexkit.JSONResponse({"message": "This route is not found"}, vortexkit.StatusCode.NOT_FOUND)

if __name__ == '__main__':
    app.run(
        host="localhost",
        port=8000,
    )