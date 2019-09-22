#!/usr/bin/env bash

set -env

docker build -t mintel-geo-app . && docker run -it --rm --name mintel-geo-running mintel-geo-app --mount source=./,target=./mintel