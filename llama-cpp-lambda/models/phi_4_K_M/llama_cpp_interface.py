import json
from llama_cpp import Llama

LLM_CLIENT_INIT = False
LLM_CLIENT = None

system_prompt = """
You are a funny person. A Real commedians commedian.
You've watched hours of Nickelodian and Cartoon Network.
You idolize SpongeBob Squarepants.
"""

prompt_formatter = lambda prompt: f"Instruct: {system_prompt}\n{prompt}\n\nOutput:"""

def handler(event, context):
    global LLM_CLIENT_INIT
    global LLM_CLIENT

    if not LLM_CLIENT_INIT:
        LLM_CLIENT = LLM_CLIENT(
            model_path="./phi-2.Q4_K_M.gguf",
            n_threads=2,
            n_ctx=2048
        )
        LLM_CLIENT_INIT = True

    body = event.get('body', '')

    ai_out = llm(
            prompt_formatter(body), 
            max_tokens=200,
            temperature=0.8
        )

    response = {
        "statusCode": 200,
        "body": ai_out
    }
    return response
    