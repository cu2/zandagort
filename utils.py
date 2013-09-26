"""
Utility functions
"""

import random


def multi_config(common_value, enum_):
    """Used in config to copy common values for all planet classes"""
    return {key: common_value.copy() for key in enum_.get_all_values()}


def generate_random_hexstring(length=32):
    """
    Generate random hex string
    
    Idea from: http://stackoverflow.com/questions/2782229/most-lightweight-way-to-create-a-random-string-and-a-random-hexadecimal-number/2782859#2782859
    """
    return ("%0" + str(length) + "x") % random.randrange(16**length)


def public(func):
    """Decorator to annotate function (typically controller method) as public"""
    func.is_public = True
    return func


def create_request_string(method, command, arguments):
    """Return request_string for client request"""
    if method == "GET":
        try:
            query_string = "&".join([key+"="+value for key, value in arguments.iteritems()])
        except Exception:
            query_string = "[ERROR]"
        request_string = "[" + method + "] " + command + ("?" + query_string if query_string != "" else "")
    else:
        request_string = "[" + method + "] " + command
    return request_string
