from vortexkit import App, Request, JSONResponse

app = App()

@app.route("/")
def index(request: Request):
    return JSONResponse({"message": "Hello, world!"})

@app.route("/interaction-callback")
def interaction_callback(request: Request):
    if not request.method == "POST":
        return JSONResponse({"error": "Method not allowed"}, status_code="405 Method Not Allowed")
    
    if not type(request.body) == dict:
        return JSONResponse({"error": "Request body must be JSON"}, status_code="400 Bad Request")
    
    if request.body["type"] not in range(1,10):
        return JSONResponse({"error": "Invalid interaction type"}, status_code="400 Bad Request")
    
    if request.body["type"] == 1:
        return JSONResponse({
            "type": 1
        })

    else:
        return JSONResponse({
            "type": 4,
            "data": {
                "tts": False,
                "content": "Congrats on sending your command!",
                "embeds": [],
                "allowed_mentions": { "parse": [] }
            }
        })

if __name__ == '__main__':
    app.run(
        host="localhost",
        port=8000,
    )