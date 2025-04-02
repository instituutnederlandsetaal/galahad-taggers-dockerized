# load the .env file
source .env

# Set the default label
: ${VERSION:=latest}

echo "Will build taggers with version <$VERSION>. Set VERSION to override this."

# Base image
docker build -t instituutnederlandsetaal/galahad-taggers-base:$VERSION base

# PIE
# base
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=cpu -t instituutnederlandsetaal/galahad-taggers-pie-cpu-base:$VERSION pie/base
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=gpu -t instituutnederlandsetaal/galahad-taggers-pie-gpu-base:$VERSION pie/base
# all
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=cpu -t instituutnederlandsetaal/galahad-taggers-pie-cpu-tdn-all:$VERSION pie/TDN-ALL
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=gpu -t instituutnederlandsetaal/galahad-taggers-pie-gpu-tdn-all:$VERSION pie/TDN-ALL
# tdn-1200-1600
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=cpu -t instituutnederlandsetaal/galahad-taggers-pie-cpu-tdn-1200-1600:$VERSION pie/TDN-1200-1600
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=gpu -t instituutnederlandsetaal/galahad-taggers-pie-gpu-tdn-1200-1600:$VERSION pie/TDN-1200-1600
# tdn-1600-1900
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=cpu -t instituutnederlandsetaal/galahad-taggers-pie-cpu-tdn-1600-1900:$VERSION pie/TDN-1600-1900
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=gpu -t instituutnederlandsetaal/galahad-taggers-pie-gpu-tdn-1600-1900:$VERSION pie/TDN-1600-1900

# UD-parsers
# flair
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=cpu -t instituutnederlandsetaal/galahad-taggers-flair-cpu:$VERSION flair
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=gpu -t instituutnederlandsetaal/galahad-taggers-flair-gpu:$VERSION flair
# # spacy
#docker build --build-arg VERSION=$VERSION --build-arg SPACY_MODEL=nl_core_news_lg --build-arg CPU_GPU=cpu -t instituutnederlandsetaal/galahad-taggers-spacy-cpu:$VERSION spacy
# docker build --build-arg VERSION=$VERSION --build-arg SPACY_MODEL=nl_core_news_lg --build-arg CPU_GPU=gpu -t instituutnederlandsetaal/galahad-taggers-spacy-gpu:$VERSION spacy
# stanza
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=cpu -t instituutnederlandsetaal/galahad-taggers-stanza-cpu:$VERSION stanza
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=gpu -t instituutnederlandsetaal/galahad-taggers-stanza-gpu:$VERSION stanza
# udpipe
# docker build --build-arg VERSION=$VERSION -t instituutnederlandsetaal/galahad-taggers-udpipe:$VERSION udpipe
# docker build --build-arg VERSION=$VERSION -t instituutnederlandsetaal/galahad-taggers-stanza:$VERSION stanza

# Huggingface
# TODO