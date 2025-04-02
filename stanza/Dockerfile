ARG VERSION=dev
FROM instituutnederlandsetaal/galahad-taggers-base:$VERSION

ARG CPU_GPU=cpu
ENV CPU_GPU=${CPU_GPU}

COPY --link process.py conllu_tei_helper.py ./requirements/$CPU_GPU.txt ./
RUN pip install --no-cache-dir -r $CPU_GPU.txt

# Install stanza model
# alpino + conll02 NER
RUN python -c 'import stanza; stanza.Pipeline(lang="nl", processors={"tokenize": "alpino","lemma": "alpino","pos": "alpino","depparse": "alpino","ner": "conll02"})'
# lassysmall + wiki-ner
RUN python -c 'import stanza; stanza.Pipeline(lang="nl", processors={"tokenize": "lassysmall","lemma": "lassysmall","pos": "lassysmall","depparse": "lassysmall","ner": "wikiner"})'
