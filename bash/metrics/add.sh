#!/bin/bash

NAME=${1:-}
TYPE=${2:-}
DURATION=${3:-}

curl -X POST http://127.0.0.1:5000/api/metrics \
-H "Content-Type: application/json" \
-d "{\"name\":\"$NAME\",\"type\":\"$TYPE\",\"duration\":\"$DURATION\"}" \
-b ../cookies.txt


