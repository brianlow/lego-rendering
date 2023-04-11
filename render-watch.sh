#!/bin/bash

set -e

find . -name '*.py' | entr ./render.sh
