ARG VERSION=dev
FROM instituutnederlandsetaal/taggers-dockerized-base:$VERSION

# setuptools
RUN apt-get update && apt-get install -y gcc g++
RUN pip install -U pip setuptools wheel

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --link process.py /
COPY --link pie/ ./pie/