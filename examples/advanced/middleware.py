from ...vortexkit import Middleware, Request, JSONResponse, StatusCode
import requests
import urllib.parse

class MainMiddleware(Middleware):
    def process_request(self, request: Request):
        ## check what country the request is coming from
        ## and set it in the request context
        ip = request.remote_addr or request.real_ip

        if not ip:
            return JSONResponse({"message": "No IP address found"}, StatusCode.BAD_REQUEST)
        
        ## make ip url encoded
        safe_ip = urllib.parse.quote_plus(ip)

        response = requests.get(f"http://ip-api.com/json/{safe_ip}")

        if response.status_code == 200:
            request.context.country = response.json().get("country")
        else:
            request.context.country = "Unknown"
