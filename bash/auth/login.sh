#!/bin/bash

LOGIN=${1:""}
PASSWORD=${2:""}

curl -X POST http://127.0.0.1:5000/api/login \
-H "Content-Type: application/json" \
-d "{\"login\":\"${LOGIN}\",\"password\":\"${PASSWORD}\"}" \
-c ../cookies.txt
