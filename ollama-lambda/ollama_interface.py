import json
import ollama

client = ollama.Client(host='http://0.0.0.0:11434')

def handler(event, context):

    body = event.get('body', '')

    # Wakes the model for all invocations
    ai_out = client.generate(model='lambda-model:latest', prompt=body)

    response = {
        "statusCode": 200,
        "body": ai_out
    }
    return response
    