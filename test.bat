call .\build.bat

docker volume create mitosisdetection-output

docker run --rm^
 --memory=16g^
 -v %~dp0\test\:/input/^
 -v mitosisdetection-output:/output/^
 mitosisdetection

docker run --rm^
 -v mitosisdetection-output:/output/^
 python:3.7-slim cat /output/mitotic_figures.json | python -m json.tool

docker run --rm^
 -v mitosisdetection-output:/output/^
 -v %~dp0\test\:/input/^
 python:3.7-slim python -c "import json, sys; f1 = json.load(open('/output/mitotic_figures.json')); f2 = json.load(open('/input/expected_output.json')); sys.exit(f1 != f2);"

if %ERRORLEVEL% == 0 (
	echo "Tests successfully passed..."
)
else
(
	echo "Expected output was not found..."
)

docker volume rm mitosisdetection-output
