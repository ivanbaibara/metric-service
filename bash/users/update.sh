#!/bin/bash

NEW_PASSWORD=${1:-}

curl -X PATCH http://127.0.0.1:5000/api/users \
-H "Content-Type: application/json" \
-d "{\"password\":\"$NEW_PASSWORD\"}" \
-b ../cookies.txt