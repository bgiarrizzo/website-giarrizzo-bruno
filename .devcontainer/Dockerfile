ARG VARIANT="3"
FROM python:${VARIANT}

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /workspaces/app/

WORKDIR /workspaces/app/
EXPOSE 8000

# Prepare Base System
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt update \
    && apt-get install -y build-essential gcc libssl-dev

# Configure Base Python
RUN python -m pip --disable-pip-version-check --no-cache-dir install --upgrade pip \
    && python -m pip --disable-pip-version-check --no-cache-dir install --upgrade pipenv \
    && python -m pip install --upgrade setuptools 

# Cleanup
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/tmp/* \
    && rm -rf /tmp/*
