# load the .env file
source .env

# Set the default label
: ${VERSION:=latest}
: ${CPU_GPU:=cpu}

echo "Will build taggers with version <$VERSION> and CPU_GPU <$CPU_GPU>. Set .env to override this."

./build.sh

# PIE
docker push instituutnederlandsetaal/galahad-taggers-pie-tdn-1200-1600:$CPU_GPU-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-pie-tdn-1600-1900:$CPU_GPU-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-pie-tdn-all:$CPU_GPU-$VERSION

# UD-parsers
docker push instituutnederlandsetaal/galahad-taggers-spacy:$CPU_GPU-$VERSION

# Huggingface
docker push instituutnederlandsetaal/galahad-taggers-hug-tdn-1400-1600:$CPU_GPU-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-hug-tdn-1600-1900:$CPU_GPU-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-hug-tdn-all:$CPU_GPU-$VERSION
docker push instituutnederlandsetaal/galahad-taggers-hug-tdn-all-enhanced:$CPU_GPU-$VERSION
