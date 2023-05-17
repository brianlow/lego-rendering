#!/bin/bash

set -e

/Applications/Blender.app/Contents/MacOS/Blender --background --python ./setup.py

cd /Applications/Blender.app/Contents/Resources/3.5/python/bin

./python3.10 -m pip install pillow
