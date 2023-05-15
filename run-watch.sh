#!/bin/bash

set -e

find . -name '*.py' | entr ./run.sh $1
