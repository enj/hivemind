#!/bin/sh

coverage run --source hivemind -m unittest discover . -v
coverage report -m --omit "*/__init__.py"
