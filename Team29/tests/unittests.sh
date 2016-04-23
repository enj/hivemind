#!/bin/sh

coverage run --source hivemind --omit "*/__init__.py" -m unittest discover . -v
coverage report
