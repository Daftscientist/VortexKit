from WhirlWind import App, responses
## Imports ^


app = App(staticFolder="static")
## Initial app setup ^

@app.path('/')
## Creating a route ^
def index():
## Defining the function ^
    return responses.HtmlResponse("<a href='/'>Link Back To Home</a>")
    ## Returning your chosen response ^

if __name__ == "__main__":
## To check the file is ran ^
    app.run("localhost", 5000)
    ## Running the webserver ^
