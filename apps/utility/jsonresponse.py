
def success_response(status, data):
    """Success JSON Response"""
    response = {
        "code" : status,
        "results" : data
    }
    return response


def error_response(status, data):
    """Error JSON Response"""
    response = {
        "code" : status,
        "message" : data
    }
    return response