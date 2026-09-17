ARG VERSION=dev

FROM instituutnederlandsetaal/galahad-taggers:$VERSION

ARG CPU_GPU=cpu
ENV CPU_GPU=$CPU_GPU

RUN --mount=type=bind,source=requirements/$CPU_GPU.txt,target=requirements.txt \
    --mount=type=bind,source=nltk-download.py,target=nltk-download.py \
    pip install --no-deps --no-cache -r requirements.txt \
    --extra-index-url "$([ "$CPU_GPU" = "gpu" ] && echo https://download.pytorch.org/whl/cu126 || echo https://download.pytorch.org/whl/cpu)" && \
    python nltk-download.py

COPY --link process.py /
COPY --link model.config /
COPY --link ./lemmatizer ./lemmatizer
COPY --link ./lexicon ./lexicon
COPY --link ./huggingface/lemmatizer ./huggingface/lemmatizer
COPY --link ./huggingface/tagging ./huggingface/tagging
