from ckan.logic.schema import validator_args


@validator_args
def order_ticket(not_empty, ignore_empty, fpx_base64_json_if_string):
    return {
        "type": [not_empty],
        "items": [not_empty, fpx_base64_json_if_string],
        "options": [ignore_empty, fpx_base64_json_if_string],
    }
