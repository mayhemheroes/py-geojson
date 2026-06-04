# Build Stage
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    clang \
    git \
    && rm -rf /var/lib/apt/lists/*

ENV CC=clang CXX=clang++

RUN pip install --no-cache-dir atheris

ADD . /src
WORKDIR /src
RUN python3 -m pip install .

CMD ["/src/mayhem/fuzz_lib.py"]
