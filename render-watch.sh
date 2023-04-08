#!/bin/bash

set -e

find . | entr ./render.sh
