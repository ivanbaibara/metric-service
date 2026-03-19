#!/bin/bash

ID=${1:-}
NAME=${2:-}
DURATION=${3:-}

curl -X PATCH http://127.0.0.1:5000/api/metrics \
-H "Content-Type: application/json" \
-d "{\"id\":\"$ID\",\"name\":\"$NAME\",\"duration\":\"$DURATION\"}" \
-b ../cookies.txt
