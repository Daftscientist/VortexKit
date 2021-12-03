from WhirlWind import App, responses
## Imports ^


app = App(staticFolder="static")
## Initial app setup ^

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
def plainText():
    return responses.FileResponse("test.json")

if __name__ == "__main__":
    app.run("localhost", 5000)
    ## Running the webserver ^
