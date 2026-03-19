#!/bin/bash

ROLE=${1:-}
LOGIN=${2:-}
PASSWORD=${3:-}

curl -X POST http://127.0.0.1:5000/api/users \
-H "Content-Type: application/json" \
-d "{\"role\":\"$ROLE\",\"login\":\"$LOGIN\",\"password\":\"$PASSWORD\"}" \
-b ../cookies.txt