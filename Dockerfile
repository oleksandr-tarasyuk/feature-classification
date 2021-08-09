FROM python:3.7-slim as builder

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install
# --deploy

# Stage 2: Runtime
FROM debian:buster-slim
ARG PYTHON_VERSION=3.7

RUN apt update && \
    apt install --no-install-recommends -y build-essential python3 && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /.venv/lib/python${PYTHON_VERSION}/site-packages/ /usr/local/lib/python${PYTHON_VERSION}/dist-packages/

COPY package_name /package_name
COPY fluid/fluid_service.py fluid_service.py

CMD ["python3", "fluid_service.py"]
