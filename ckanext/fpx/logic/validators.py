import binascii
import base64
import json

import ckan.plugins.toolkit as tk


def get_validators():
    return {
        "fpx_base64_json_if_string": base64_json_if_string,
    }


def base64_json_if_string(value):
    if not isinstance(value, str):
        return value
    binary = bytes(value, "utf8")

    try:
        decoded = base64.decodebytes(binary)
    except binascii.Error:
        raise tk.Invalid("Must be a base64-encoded")
    try:
        return json.loads(decoded)
    except ValueError:
        raise tk.Invalid("Does not contain valid JSON")
