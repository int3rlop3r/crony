#!/bin/bash
find . -name "*.pyc" -exec rm -rf {} \;
find . -name "__pycache__" -exec rmdir {} \;
