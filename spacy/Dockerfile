ARG VERSION=dev
FROM instituutnederlandsetaal/taggers-dockerized-base:$VERSION

# setuptools
RUN apt-get update && apt-get install -y gcc g++
RUN pip install -U pip setuptools wheel

# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install spacy model
ARG SPACY_MODEL
ENV SPACY_MODEL=${SPACY_MODEL}
RUN python3 -m spacy download ${SPACY_MODEL}

# tagger specific python source
COPY --link process.py conllu_tei_helper.py ./

# fix cuda env
COPY --link fix-cuda-env.sh ./
RUN ./fix-cuda-env.sh
