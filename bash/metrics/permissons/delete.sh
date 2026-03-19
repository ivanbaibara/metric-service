#!/bin/bash

ID=${1:-}
USER_LOGIN=${2:-}

curl -X DELETE http://127.0.0.1:5000/api/metrics/permissions \
-H "Content-Type: application/json" \
-d "{\"id\":\"$ID\",\"user_login\":\"$USER_LOGIN\"}" \
-b ../cookies.txt
