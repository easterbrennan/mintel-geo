#!/bin/bash

docker build -t mintel-geo-image . && docker run -it --rm -v json_output:/mintel-geo/json_output/ --name mintel-geo mintel-geo-image python mintel.py
