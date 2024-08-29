BAD_REQUEST_EXCEPTION = {
    "errors": [{"status": 400, "title": "BadRequest"}],
}

UNAUTHORIZED_EXCEPTION = {
    "errors": [{"status": 401, "title": "Unauthorized"}],
}

FORBIDDEN_EXCEPTION = {
    "errors": [{"status": 403, "title": "Forbidden"}],
}

RESOURCE_NOT_FOUND_EXCEPTION = {
    "errors": [{"status": 404, "title": "NotFound"}],
}

SERVER_ERROR_EXCEPTION = {
    "errors": [{"status": 500, "title": "InternalServerError"}],
}

ERROR_EXCEPTION = {
    "errors": [{"status": 502, "title": "Error"}],
}

GATEWAY_ERROR_EXCEPTION = {
    "errors": [{"status": 503, "title": "GatewayError"}],
}
