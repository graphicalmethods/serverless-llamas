ARG FUNCTION_DIR=/var/task

FROM python:3.11.7-bookworm as base_image

ARG MODEL_PATH
ARG MODEL_GGUF
ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}

COPY requirements.txt ${FUNCTION_DIR}

RUN apt update && apt install -y gcc g++ cmake

RUN pip install --target ${FUNCTION_DIR} -r ${FUNCTION_DIR}/requirements.txt
RUN CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install --target ${FUNCTION_DIR} llama-cpp-python

RUN pip install \
    --target ${FUNCTION_DIR} \
        awslambdaric

COPY ${MODEL_PATH} ${FUNCTION_DIR}

COPY entrypoint.sh ${FUNCTION_DIR}
RUN chmod +x ${FUNCTION_DIR}/entrypoint.sh

FROM python:3.11.7-slim-bookworm

ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}

COPY --from=base_image ${FUNCTION_DIR} ${FUNCTION_DIR}

ENTRYPOINT ["/var/task/entrypoint.sh", "llama_cpp_interface.handler"]
