ARG VERSION=dev
ARG CPU_GPU=cpu

FROM instituutnederlandsetaal/galahad-taggers-base:$CPU_GPU-$VERSION

ARG SPACY_MODEL
ENV SPACY_MODEL=$SPACY_MODEL
ENV CPU_GPU=$CPU_GPU

COPY --link process.py conllu_tei_helper.py fix-cuda-env.sh requirements/$CPU_GPU.txt ./
RUN uv pip install --system --index-strategy=unsafe-best-match --no-deps --no-cache-dir -r $CPU_GPU.txt && python3 -m spacy download $SPACY_MODEL
