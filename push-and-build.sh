# Set the default label
: ${VERSION:=dev}

echo "Will build taggers with version <$VERSION>. Set VERSION to override this."

./build.sh

# PIE
docker push instituutnederlandsetaal/galahad-taggers-pie-tdn-1200-1600:cpu-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-pie-tdn-1200-1600:gpu-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-pie-tdn-1600-1900:cpu-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-pie-tdn-1600-1900:gpu-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-pie-tdn-all:cpu-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-pie-tdn-all:gpu-$VERSION

# UD-parsers
# docker push instituutnederlandsetaal/galahad-taggers-udpipe:$VERSION
docker push instituutnederlandsetaal/galahad-taggers-spacy:cpu-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-spacy:gpu-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-stanza:cpu-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-stanza:gpu-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-flair:cpu-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-flair:gpu-$VERSION

# Huggingface
# Commented for now, as we need Git LFS to build these. Perhaps in the future.
# docker push instituutnederlandsetaal/galahad-taggers-hug-tdn-1400-1600:$VERSION
# docker push instituutnederlandsetaal/galahad-taggers-hug-tdn-1600-1900:$VERSION
# docker push instituutnederlandsetaal/galahad-taggers-hug-tdn-all:$VERSION
# docker push instituutnederlandsetaal/galahad-taggers-hug-tdn-all-enhanced:$VERSION
# docker push instituutnederlandsetaal/galahad-taggers-hug-tdn-bab:$VERSION
# docker push instituutnederlandsetaal/galahad-taggers-hug-tdn-clvn:$VERSION
# docker push instituutnederlandsetaal/galahad-taggers-hug-tdn-cour:$VERSION
# docker push instituutnederlandsetaal/galahad-taggers-hug-tdn-dbnldq:$VERSION
