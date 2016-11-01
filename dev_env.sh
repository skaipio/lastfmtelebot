#!/bin/bash
# Source this before executing 'flask run'
# Assumes local_config.py is present
export FLASK_APP=api.py
export FLASK_DEBUG=1
export LASTFMBOTAPI_CONFIG="./local_config.py"
