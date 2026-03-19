#!/bin/bash

ID=${1:-}

curl -X DELETE http://127.0.0.1:5000/api/metrics \
-H "Content-Type: application/json" \
-d "{\"id\":\"$ID\"}" \
-b ../cookies.txt