# Stage 1: Builder/Compiler
FROM python:3.7-slim as builder

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

## Save dependencies in /.venv
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install # --deploy

# Stage 2: Runtime
ARG CUDA=10.1
ARG CUDNN=7
ARG PYTHON_VERSION=3.7

FROM nvidia/cuda:${CUDA}-cudnn${CUDNN}-runtime

RUN apt update && \
    apt install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install --no-install-recommends -y python${PYTHON_VERSION} python3-distutils && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 2 && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /.venv/lib/python${PYTHON_VERSION}/site-packages/  /usr/local/lib/python${PYTHON_VERSION}/dist-packages

COPY package_name /package_name

COPY fluid/fluid_service.py fluid_service.py
COPY get_available_gpu.sh get_available_gpu.sh

RUN chmod +x get_available_gpu.sh
ENTRYPOINT [ "./get_available_gpu.sh" ]
CMD ["python3", "fluid_service.py"]
