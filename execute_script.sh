#!/bin/bash
python execute.py \
    -f ./data/AIS_data \
    -x ./web/XML \
    -j ./web/JSON \
    -db ./web/DB \
    -v True
