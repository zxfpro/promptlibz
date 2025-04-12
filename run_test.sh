#!/bin/bash

#pytest-html

project="promptlib"
uv run pytest --html=$test_html_path/$project.html
