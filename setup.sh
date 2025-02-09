#!/bin/bash

set -e

export BLENDER_VERSION=4.3

/Applications/Blender.app/Contents/MacOS/Blender --background --python ./setup.py

cd /Applications/Blender.app/Contents/Resources/${BLENDER_VERSION}/python/bin

./python3.11 -m pip install pillow
