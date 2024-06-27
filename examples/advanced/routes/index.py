
from ....vortexkit.enums import StatusCode
from ....vortexkit import Request
from ....vortexkit.responses import PlainTextResponse


def index_route(request: Request):
    return PlainTextResponse(f"Hello, your requesting from {request.context.country}", StatusCode.OK)