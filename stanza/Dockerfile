ARG VERSION=dev
FROM instituutnederlandsetaal/taggers-dockerized-base:$VERSION

# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install stanza model
# alpino + conll02 NER
RUN python -c 'import stanza; stanza.Pipeline(lang="nl", processors={"tokenize": "alpino","lemma": "alpino","pos": "alpino","depparse": "alpino","ner": "conll02"})'
# lassysmall + wiki-ner
RUN python -c 'import stanza; stanza.Pipeline(lang="nl", processors={"tokenize": "lassysmall","lemma": "lassysmall","pos": "lassysmall","depparse": "lassysmall","ner": "wikiner"})'

# tagger specific python source
COPY --link process.py conllu_tei_helper.py ./
