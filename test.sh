#!/usr/bin/env bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

./build.sh

docker volume create mitosisdetection-output

docker run --rm --gpus all \
        --memory=16g \
        -v $SCRIPTPATH/test/:/input/images/histopathology-roi-cropout/ \
        -v mitosisdetection-output:/output/ \
        mitosisdetection

docker run --rm \
        -v mitosisdetection-output:/output/ \
        python:3.7-slim cat /output/mitotic-figures.json | python -m json.tool

docker run --rm \
        -v mitosisdetection-output:/output/ \
        -v $SCRIPTPATH/test/:/input/images/histopathology-roi-cropout/ \
        python:3.7-slim python -c "import json, sys; f1 = json.load(open('/output/mitotic-figures.json')); f2 = json.load(open('/input/images/histopathology-roi-cropout/expected_output.json')); sys.exit(f1 != f2);"

if [ $? -eq 0 ]; then
    echo "Tests successfully passed..."
else
    echo "Expected output was not found..."
fi

docker volume rm mitosisdetection-output
