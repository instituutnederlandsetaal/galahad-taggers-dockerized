# load the .env file
source .env

# Set the default label
: ${VERSION:=latest}
: ${CPU_GPU:=cpu}

echo "Will build taggers with version <$VERSION> and CPU_GPU <$CPU_GPU>. Set .env to override this."

# Base image
docker build -t instituutnederlandsetaal/galahad-taggers:$VERSION base

# PIE
# base
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=$CPU_GPU -t instituutnederlandsetaal/galahad-taggers-pie:$CPU_GPU-$VERSION pie/base
# tdn-all
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=$CPU_GPU -t instituutnederlandsetaal/galahad-taggers-pie-tdn-all:$CPU_GPU-$VERSION pie/TDN-ALL
# tdn-1200-1600
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=$CPU_GPU -t instituutnederlandsetaal/galahad-taggers-pie-tdn-1200-1600:$CPU_GPU-$VERSION pie/TDN-1200-1600
# tdn-1600-1900
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=$CPU_GPU -t instituutnederlandsetaal/galahad-taggers-pie-tdn-1600-1900:$CPU_GPU-$VERSION pie/TDN-1600-1900

# UD-parsers
# spacy
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=$CPU_GPU --build-arg SPACY_MODEL=nl_core_news_lg -t instituutnederlandsetaal/galahad-taggers-spacy:$CPU_GPU-$VERSION spacy

# Huggingface
# base
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=$CPU_GPU -t instituutnederlandsetaal/galahad-taggers-hug:$CPU_GPU-$VERSION huggingface/base
# tdn-all
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=$CPU_GPU -t instituutnederlandsetaal/galahad-taggers-hug-tdn-all:$CPU_GPU-$VERSION huggingface/TDN-ALL
# tdn-all-enhanced
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=$CPU_GPU -t instituutnederlandsetaal/galahad-taggers-hug-tdn-all-enhanced:$CPU_GPU-$VERSION huggingface/TDN-ALL-ENHANCED
# tdn-1400-1600
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=$CPU_GPU -t instituutnederlandsetaal/galahad-taggers-hug-tdn-1400-1600:$CPU_GPU-$VERSION huggingface/TDN-1400-1600
# tdn-1600-1900
docker build --build-arg VERSION=$VERSION --build-arg CPU_GPU=$CPU_GPU -t instituutnederlandsetaal/galahad-taggers-hug-tdn-1600-1900:$CPU_GPU-$VERSION huggingface/TDN-1600-1900

