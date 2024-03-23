include .env

MODEL_NAME=$(shell echo $(word 2,$(subst /, ,$(MODEL_PATH))) | tr A-Z a-z)
IMAGE_TAG=${IMAGE}/$(MODEL_NAME):`git rev-parse --short HEAD`

.PHONY: aws-cli-validator
aws-cli-validator:
	@which aws > /dev/null || echo "AWS CLI NOT FOUND"

.PHONY: requirements
requirements:
	@pip freeze --exclude-editable > requirements.txt

.PHONY: docker-build
docker-build: requirements
	@docker build --platform linux/arm64 --build-arg MODEL_PATH=${MODEL_PATH} . -t ${IMAGE_TAG}

.PHONY: docker-run
docker-run:
	@docker run --rm -p 9000:8080 \
		--platform linux/arm64 \
		-v ~/.aws-lambda-rie:/aws-lambda \
		${IMAGE_TAG}

.PHONY: docker-test
docker-test:
	@curl -H "Content-Type: application/json" "http://localhost:9000/2015-03-31/functions/function/invocations" -d @tests/prompt.json

.PHONY: fetch-model
fetch-model:
	@huggingface-cli download ${MODEL_REPO} ${MODEL_GGUF} --local-dir ${MODEL_PATH} --local-dir-use-symlinks False
