#!/bin/bash

docker build -t mintel-geo-image . && docker run -it --rm --name mintel-geo mintel-geo-image python mintel.py
