ARG VERSION=dev
FROM instituutnederlandsetaal/taggers-dockerized-base:$VERSION

COPY --link ./process.py ./requirements.txt  ./
COPY --link ./pie/ ./pie/
RUN pip install --no-deps --no-cache-dir -r requirements.txt