ARG VERSION=dev
ARG CPU_GPU=cpu

FROM instituutnederlandsetaal/galahad-taggers-base:$CPU_GPU-$VERSION

ENV CPU_GPU=$CPU_GPU

COPY --link ./process.py ./requirements/$CPU_GPU.txt ./
RUN uv pip install --system --index-strategy=unsafe-best-match --no-deps --no-cache-dir -r $CPU_GPU.txt && python -c 'from flair.nn import Classifier; Classifier.load("flair/upos-multi"); Classifier.load("flair/ner-dutch-large")'
