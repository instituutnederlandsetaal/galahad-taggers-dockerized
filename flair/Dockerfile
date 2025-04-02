ARG VERSION=dev
FROM instituutnederlandsetaal/galahad-taggers-base:$VERSION

ARG CPU_GPU=cpu
ENV CPU_GPU=${CPU_GPU}

COPY --link ./process.py ./requirements/$CPU_GPU.txt ./
RUN uv pip install --system --index-strategy=unsafe-best-match --no-deps --no-cache-dir -r $CPU_GPU.txt && python -c 'from flair.nn import Classifier; Classifier.load("flair/upos-multi"); Classifier.load("flair/ner-dutch-large")'
