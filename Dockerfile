# syntax=docker/dockerfile:1

# Stage: build Python environment
FROM python:3.11-slim AS python-builder

ENV VENV_PATH=/opt/venv

RUN python -m venv ${VENV_PATH} \
    && ${VENV_PATH}/bin/pip install --upgrade pip

ENV PATH="${VENV_PATH}/bin:${PATH}"

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade wheel setuptools \
    && pip install --no-cache-dir -r requirements.txt

# Optional Node stage can be added here if a package.json exists in the project root.
# FROM node:20-slim AS node-builder
# WORKDIR /app
# COPY package*.json ./
# RUN npm install --production
# COPY . .
# RUN npm run build
# The build output should then be copied from /app/dist (or similar) to /opt/node in the final stage.

FROM gcr.io/distroless/python3-debian12

ENV PATH="/opt/venv/bin:${PATH}"
WORKDIR /app

COPY --from=python-builder /opt/venv /opt/venv
COPY --from=python-builder /bin/bash /bin/bash

COPY . .

EXPOSE 8080

CMD ["./start.sh"]
