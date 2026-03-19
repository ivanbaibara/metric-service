#!/bin/bash

ID=${1:-}

curl -X GET http://127.0.0.1:5000/api/metrics?id=$ID -b ../cookies.txt