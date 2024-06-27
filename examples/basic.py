import vortexkit

app = vortexkit.App()

@app.route("/")
def home(request: vortexkit.Request):
    return vortexkit.PlainTextResponse("Hello, World!", vortexkit.StatusCode.OK)

if __name__ == '__main__':
    app.run(
        host="localhost",
        port=8000,
    )