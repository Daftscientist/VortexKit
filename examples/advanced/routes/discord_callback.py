from ....vortexkitvortexkit import Request, JSONResponse, StatusCode, Route
from dishookr import InteractionResponse, InteractionResponseType, InteractionCallbackMessage

class DiscordCallback(Route):
    def __init__(self):
        self.path = "/discord_callback"
        self.handler = self.discord_callback

    def discord_callback(request: Request):
        if not request.method == "POST":
            return JSONResponse({"error": "Method not allowed"}, status_code=StatusCode.BAD_REQUEST)
        
        if not request.body["type"] == 3 and not request.body["data"]["custom_id"] == "button1":
            return JSONResponse({"error": "Invalid interaction type"}, status_code=StatusCode.BAD_REQUEST)
        
        my_dishook_response = InteractionResponse(
            type=InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data=InteractionCallbackMessage(
                content="You clicked the button!"
            )
        )

        return JSONResponse(
            my_dishook_response.__dict__(), status_code=StatusCode.OK
        )