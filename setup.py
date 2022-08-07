# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    package_data={"ckanext.fpx": ["assets/**/*"]},
    message_extractors={
        "ckanext": [
            ("**.py", "python", None),
            ("**.js", "javascript", None),
            ("**/templates/**.html", "ckan", None),
        ],
    },
)
