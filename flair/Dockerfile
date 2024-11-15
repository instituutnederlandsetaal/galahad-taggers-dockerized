ARG VERSION=dev
FROM instituutnederlandsetaal/taggers-dockerized-base:$VERSION

# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install flair model
RUN python -c 'from flair.nn import Classifier; Classifier.load("flair/upos-multi"); Classifier.load("flair/ner-dutch-large")'

# tagger specific python source
COPY --link process.py ./