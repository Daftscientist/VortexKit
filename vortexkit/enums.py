from enum import Enum

class StatusCode(Enum):
    OK = "200 OK"
    BAD_REQUEST = "400 Bad Request"
    UNAUTHORIZED = "401 Unauthorized"
    FORBIDDEN = "403 Forbidden"
    NOT_FOUND = "404 Not Found"
    INTERNAL_SERVER_ERROR = "500 Internal Server Error"
    NOT_IMPLEMENTED = "501 Not Implemented"
    BAD_GATEWAY = "502 Bad Gateway"
    SERVICE_UNAVAILABLE = "503 Service Unavailable"
    GATEWAY_TIMEOUT = "504 Gateway Timeout"
    HTTP_VERSION_NOT_SUPPORTED = "505 HTTP Version Not Supported"
    NETWORK_AUTHENTICATION_REQUIRED = "511 Network Authentication Required"
    UNKNOWN_ERROR = "520 Unknown Error"
    WEB_SERVER_IS_DOWN = "521 Web Server Is Down"
    CONNECTION_TIMED_OUT = "522 Connection Timed Out"
    ORIGIN_IS_UNREACHABLE = "523 Origin Is Unreachable"
    A_TIMEOUT_OCCURRED = "524 A Timeout Occurred"
    SSL_HANDSHAKE_FAILED = "525 SSL Handshake Failed"
    INVALID_SSL_CERTIFICATE = "526 Invalid SSL Certificate"

