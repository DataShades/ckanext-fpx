#!/bin/bash
set -e

pytest --ckan-ini=subdir/test.ini --cov=ckanext.fpx ckanext/fpx/tests
