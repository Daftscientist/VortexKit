from WhirlWind import App

app = App(host="localhost", port=80, secretKey="NoLeakOrIStealYourCookies")

@app.path('/')
def index():
    return 'This is the index page of the website.'
