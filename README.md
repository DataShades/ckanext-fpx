# ckanext-fpx

CKAN adapter for FPX service

## Requirements

- Configured and running FPX

## Installation

To install ckanext-fpx:

1. Activate your CKAN virtual environment

1. Install the ckanext-fpx Python package:

		pip install ckanext-fpx

1. Add ``fpx`` to the ``ckan.plugins`` setting in your CKAN config file

1. Add ``fpx.client.secret`` and ``fpx.service.url`` config options

## Config settings

    # Client secret generated by FPX
    # (required).
	fpx.client.secret = 123abc

    # Name corresponding to the secret. Required only for file-streaming.
    # (optional).
	fpx.client.secret = client-name-for-123abc-secret


    # URL of the running FPX service
    # (required).
    fpx.service.url = http://0.0.0.0:8000
