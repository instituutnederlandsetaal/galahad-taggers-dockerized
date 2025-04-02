ARG VERSION=dev
FROM instituutnederlandsetaal/galahad-taggers-base:$VERSION

# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# tagger specific python source
COPY --link ./models ./models
COPY --link process.py wembeddings.py udpipe2_server.py udpipe2_eval.py udpipe2_dataset.py udpipe2.py ./
