#!/bin/bash

ID=${1:-}
VALUE=${2:-}

curl -X POST http://127.0.0.1:5000/api/data \
-H "Content-Type: application/json" \
-d "{\"id\":$ID,\"value\":$VALUE}" \
-b ../cookies.txt