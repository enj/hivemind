#!/bin/sh

coverage run --source hivemind -m unittest discover . -v
coverage report --omit "*/__init__.py"
