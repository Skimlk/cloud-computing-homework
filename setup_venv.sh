#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

SITE_PACKAGES=$(ls -d venv/lib/python*/site-packages | sort | tail -n 1)

echo "$PWD" > "$SITE_PACKAGES/${PWD##*/}.pth" 
