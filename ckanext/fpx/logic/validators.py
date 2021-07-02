import binascii
import base64
import json

import ckan.plugins.toolkit as tk


def get_validators():
    return {
        "fpx_base64_json": base64_json,
    }


def base64_json(value):
    try:
        binary = bytes(value, "utf8")
    except TypeError:
        raise tk.Invalid("Must be a string")
    try:
        decoded = base64.decodebytes(binary)
    except binascii.Error:
        raise tk.Invalid("Must be a base64-encoded")
    try:
        return json.loads(decoded)
    except ValueError:
        raise tk.Invalid("Does not contain valid JSON")
