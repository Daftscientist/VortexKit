from enum import Enum

class StatusCode(Enum):
    """
    Enum representing HTTP status codes with their corresponding descriptions.

    Attributes:
        OK (str): 200 OK - The request has succeeded.
        BAD_REQUEST (str): 400 Bad Request - The server could not understand the request due to invalid syntax.
        UNAUTHORIZED (str): 401 Unauthorized - The request requires user authentication.
        FORBIDDEN (str): 403 Forbidden - The server understood the request, but refuses to authorize it.
        NOT_FOUND (str): 404 Not Found - The requested resource could not be found on the server.
        INTERNAL_SERVER_ERROR (str): 500 Internal Server Error - A generic error message, typically for unexpected conditions.
        NOT_IMPLEMENTED (str): 501 Not Implemented - The server does not support the functionality required to fulfill the request.
        BAD_GATEWAY (str): 502 Bad Gateway - The server received an invalid response from an inbound server.
        SERVICE_UNAVAILABLE (str): 503 Service Unavailable - The server is currently unavailable.
        GATEWAY_TIMEOUT (str): 504 Gateway Timeout - The server did not receive a timely response from an upstream server.
        HTTP_VERSION_NOT_SUPPORTED (str): 505 HTTP Version Not Supported - The server does not support the HTTP protocol version.
        NETWORK_AUTHENTICATION_REQUIRED (str): 511 Network Authentication Required - The client needs to authenticate to gain network access.
        UNKNOWN_ERROR (str): 520 Unknown Error - An unknown error occurred.
        WEB_SERVER_IS_DOWN (str): 521 Web Server Is Down - The origin server refused the connection.
        CONNECTION_TIMED_OUT (str): 522 Connection Timed Out - The server could not negotiate a TCP handshake with the origin server.
        ORIGIN_IS_UNREACHABLE (str): 523 Origin Is Unreachable - The server could not reach the origin server.
        A_TIMEOUT_OCCURRED (str): 524 A Timeout Occurred - The server successfully connected but did not receive a complete response.
        SSL_HANDSHAKE_FAILED (str): 525 SSL Handshake Failed - The server could not negotiate an SSL/TLS handshake.
        INVALID_SSL_CERTIFICATE (str): 526 Invalid SSL Certificate - The server could not validate the SSL certificate.

    Note:
        These descriptions are based on typical HTTP status code definitions.
    """

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
