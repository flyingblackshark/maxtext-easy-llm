FROM python:3.10-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV MAXTEXT_VERSION=main

RUN apt -y update && apt install -y --no-install-recommends \
    ca-certificates \
    git \
    python3.10 \
    python3-pip

RUN update-alternatives --install \
    /usr/bin/python3 python3 /usr/bin/python3.10 1

RUN git clone https://github.com/google/maxtext.git

RUN cd maxtext/ && \
git checkout ${MAXTEXT_VERSION} && \
bash setup.sh

COPY maxengine_server_entrypoint.sh /usr/bin/

RUN chmod +x /usr/bin/maxengine_server_entrypoint.sh

ENTRYPOINT ["/usr/bin/maxengine_server_entrypoint.sh"]