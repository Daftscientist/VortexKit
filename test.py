from WhirlWind import App
## Imports ^

app = App(host="localhost", port=80, secretKey="NoLeakOrIStealYourCookies")
## Initial webserver setup ^

@app.path('/')
def index():
    return 'This is the index page of the website.'
## Created a route, on the path `/`, that returns anything in the function return ^
