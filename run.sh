#!/bin/bash

set -e

"${BLENDER_DIR:-/Applications/Blender.app}/Contents/MacOS/Blender" --background --python "$1"
