from WhirlWind import App, PlainTextResponse, HtmlResponse, JSONResponse, Request

app = App()

@app.route("/")
def home(req: Request):
    return PlainTextResponse(f"Hello, World! {req.cookies}")

@app.route("/about")
def about(req: Request):
    return HtmlResponse(f"<h1>About</h1> {req.query_params}")

@app.route("/json")
def json(req):
    return JSONResponse({"message": "Hello, World! ", "form-data": req.body})

@app.route('/get-req-data')
def get_req_data(req: Request):
    return JSONResponse(req.__to_json__())

if __name__ == "__main__":
    app.run("localhost", 8080)