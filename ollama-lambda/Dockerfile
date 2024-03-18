ARG FUNCTION_DIR=/var/task

FROM python:3.11.7-bookworm as base_image

ARG MODEL_PATH
ARG FUNCTION_DIR
ENV OLLAMA_MODELS=${FUNCTION_DIR}/models/ollama
ENV HOME=/var/task

RUN mkdir -p ${FUNCTION_DIR}

COPY requirements.txt ${FUNCTION_DIR}

RUN pip install --target ${FUNCTION_DIR} -r ${FUNCTION_DIR}/requirements.txt

RUN pip install \
    --target ${FUNCTION_DIR} \
        awslambdaric

COPY ollama_interface.py ${FUNCTION_DIR}

COPY ${MODEL_PATH} /tmp

RUN curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama && \
    chmod +x /usr/bin/ollama

RUN bash -c "/usr/bin/ollama serve &" && sleep 1 && /usr/bin/ollama create lambda-model -f /tmp/Modelfile

# This is to allow the aws user to access the model files. Ollama gets executed under the aws user which
# for some reason seems to not allow ollama to use the models.
RUN chmod -R 777 ${OLLAMA_MODELS}

FROM python:3.11.7-slim-bookworm

ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}

ENV HOME=/var/task
ENV OLLAMA_MODELS=${FUNCTION_DIR}/models/ollama
ENV OLLAMA_HOST="0.0.0.0"

COPY --from=base_image ${FUNCTION_DIR} ${FUNCTION_DIR}
COPY --from=base_image /usr/bin/ /usr/bin/

COPY entrypoint.sh ${FUNCTION_DIR}
RUN chmod +x ${FUNCTION_DIR}/entrypoint.sh

ENTRYPOINT ["/var/task/entrypoint.sh", "ollama_interface.handler"]
