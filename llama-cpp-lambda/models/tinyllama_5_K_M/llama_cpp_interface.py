import json
from llama_cpp import Llama

LLM_CLIENT_INIT = False
LLM_CLIENT = None

system_prompt = """
You are a funny person. A Real commedians commedian.
You've watched hours of Nickelodian and Cartoon Network.
You idolize SpongeBob Squarepants.
"""

prompt_formatter = lambda prompt: f"<|system|>\n{system_prompt}</s>\n<|user|>\n{prompt}</s>\n<|assistant|>"""

def handler(event, context):
    global LLM_CLIENT_INIT
    global LLM_CLIENT

    if not LLM_CLIENT_INIT:
        LLM_CLIENT = Llama(
            model_path="./tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf",
            n_threads=2,
            n_ctx=2048
        )
        LLM_CLIENT_INIT = True

    body = event.get('body', '')

    ai_out = LLM_CLIENT(
            prompt_formatter(body), 
            max_tokens=200,
            temperature=0.8
        )

    response = {
        "statusCode": 200,
        "body": ai_out
    }
    return response
    