#!/bin/bash

nohup /usr/bin/ollama serve & >/dev/null 2>&1 && sleep 1

if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
    exec /aws-lambda/aws-lambda-rie /usr/local/bin/python -m awslambdaric $@
else
    exec /usr/local/bin/python -m awslambdaric $@
fi