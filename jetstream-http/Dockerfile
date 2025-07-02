FROM python:3.10-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV JETSTREAM_VERSION=main

# Install system dependencies
RUN apt-get update && apt-get install -y curl gnupg git ca-certificates

# Add the Google Cloud SDK package repository
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Install the Google Cloud SDK
RUN apt-get update && apt-get install -y google-cloud-sdk

# Set the default Python version to 3.10
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.10 1

RUN git clone https://github.com/google/JetStream.git && \
cd /JetStream && \
git checkout ${JETSTREAM_VERSION} && \
pip install -e .

RUN pip3 install uvicorn
RUN pip3 install fastapi
RUN pip3 install pydantic
ENV PYTHONDONTWRITEBYTECODE=1

COPY http_server.py /httpserver/
WORKDIR /httpserver

CMD ["uvicorn", "http_server:app", "--host=0.0.0.0", "--port=8000"]