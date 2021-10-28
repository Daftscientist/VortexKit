from WhirlWind import App
## Imports ^

myApp = App()
## Initial app setup ^

@myApp.path('/')
def index():
    return [b"Visit <a href='/test'>me</a>!"]

@myApp.path("/test")
def test():
    return [b"Hello, World!"]
## Created a route, on the path `/`, that returns anything in the function return ^

myApp.run("127.0.0.1", 5000)
## Running the webserver ^