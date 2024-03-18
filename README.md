# serverless-llamas
AWS Lambda Implementations of llama.cpp and Ollama for serverless inference.

### Background:

AWS Lambda has huge potential for deploying serverless LLMs using llama.cpp. There's minimal configuration, inherent scaling, and easy integration with the rest of AWS services. There's also a very generous free tier to help ease the cost of running an LLM.

Phi-2 and TinyLlama are small enough models to provide CPU only inference at "reasonable" inference speed. This is roughly 30s-40s init and 10s-20s for inference in testing. There should be no expectation of using this for chat, batch inference only.

There is an example in the ollama-lamdba project of using a Mistral 7b model variant: 
- openhermes-2.5-neural-chat-v3-3-slerp.Q4_K_M.gguf

This takes anywhere from 6min to 9min to load. Inference after init is more "reasonable" and around 30s-40s in testing. 

### Tested Models
- [Phi-2](https://huggingface.co/TheBloke/phi-2-GGUF)
- [Phi-2-DPO](https://huggingface.co/TheBloke/phi-2-dpo-GGUF)
- [TinyLlama](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF)
- [OpenHermes-2.5-neural-chat-v3-3-Slerp-GGUF](https://huggingface.co/TheBloke/OpenHermes-2.5-neural-chat-v3-3-Slerp-GGUF)

These are all 4_K_M quantization with the exception of TinyLlama using 5_K_M.

## Installation

This project relies on the following:
- [Serverless Framework](https://www.serverless.com/framework/docs/getting-started/)
- AWS
    - [Lambda Runtime Emulator](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions)
        - To keep image sizes smaller this is not included in the Docker image. The expectation is this is installed in the users home folder. If installed in another place edit the Makefile accordingly.
    - default profile for credentials.
- make
- docker

## Getting started
Pick which implementation you want to develop in ```ollama-lambda``` or ```llama-cpp-lambda``` and ```cd``` to the directory.

Make a virtual env and install dependencies:
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Create ```.env``` file for local development:
```bash
export IMAGE=ollama # Used in docker build as the image name.
export MODEL_REPO=TheBloke/phi-2-dpo-GGUF # Model repo for fetching models.
export MODEL_GGUF=phi-2-dpo.Q4_K_M.gguf # The model quantization to fetch.
export MODEL_PATH=models/phi_dpo_4_K_M # Path to the local location of the model. Note you must create this.
```

### Installing a New Model:
If installing a new model change to the project folder:
- Make the model path if it does not exist:
    - ```mkdir -p models/<NEW_MODEL>```
- Run ```make fetch-model``` 
    - This will download the specified model to the env var ```MODEL_PATH```

### Setting Prompts and Config
#### Ollama
If using Ollama you will need to create a model file. See the examples in the models folder. Additional parameters can be found [here](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values)

#### llama.cpp
llama.cpp does not use a model file. Instead the parameters are stored in the lambda handler. Example handlers can be found in the models folder.

### Local Development and Testing:
To develop and test locally you should have a ```.env``` file in the project directory ```ollama-lambda/.env``` or ```llama-cpp-lambda/.env```

If you wish to change the test prompt edit ```prompt.json``` in the ```tests``` folder

#### Building
To build the docker image run:
```bash
make docker-build
```
You may need to comment or uncomment model paths in .dockerignore. This prevents other models from being included in the build context and adding to an already long build time.

#### Testing
To test the docker image run to start the lambda function:
```bash
make docker-run
```

In a separate terminal run:
```bash
make docker-test
```

This will send the prompt found in ```test/prompt.json``` to the lambda function.

### Deploying Lambda:
To deploy the llama lambda to AWS change to the serverless-config directory and the model type you want to deploy.

If you wish to change the model being deployed, edit the ```config.json``` file with the correct model path.

Ensure your AWS credentials are valid and run:
```bash
sls deploy
```

This will take a few minutes most likely.

Once deployed there will be a url in the output. Copy this url and run:

```bash
curl -H "Content-Type: application/json" <LAMBDA_URL> -d @../../t
ests/prompt.json
```

This will invoke the lambda function. On first invocation, there is a substantial warmup period where the model is being loaded. This can take upwards of a minute or more. Often this is around 30s-50s. 

Occasionally, on first invocation the lambda will return an Internal Server Error. This means that you've exceeded the lambda function timeout and the model is taking a substantially long time to load. If you invoke again the model should be loaded or reloaded and return a response from the llm.

Subsequent invocations will be faster around 10s-20s for additional prompts. If the lambda function has concurrent invocations the model will be loaded for each concurrency.

Additional changes can be pushed using the same sls command:
```bash
sls deploy
```

### Removing Lambda:
To remove the lambda function, change to the serverless-config directory and the model type. Then run:
```bash
sls remove
```