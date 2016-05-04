#!/bin/sh

coverage run --source hivemind -m unittest discover . -v > /dev/null
coverage report -m --omit "*/__init__.py"
coverage html
