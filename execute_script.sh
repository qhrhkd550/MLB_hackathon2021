#!/bin/bash
python execute.py \
    -f ./data/AIS_data \
    -tr ./data/AI_train_data/538008382_SmartShipData_forAI.csv \
    -x ./web/XML \
    -j ./web/JSON \
    -db ./web/DB \
    -ai ./web/AI_result/RMSE.csv \
    -v True
