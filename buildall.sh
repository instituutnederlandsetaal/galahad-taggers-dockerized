# Set the default label
: ${VERSION_LABEL:=dev}

echo "Will build taggers with version <$VERSION_LABEL>. Set VERSION_LABEL to override this."

# Base image
docker build -t instituutnederlandsetaal/taggers-dockerized-base:$VERSION_LABEL base

# PIE
docker build -t instituutnederlandsetaal/taggers-dockerized-pie-base:$VERSION_LABEL pie/base
docker build -t instituutnederlandsetaal/taggers-dockerized-pie-bab:$VERSION_LABEL pie/bab
docker build -t instituutnederlandsetaal/taggers-dockerized-pie-tdn:$VERSION_LABEL pie/tdn
docker build -t instituutnederlandsetaal/taggers-dockerized-pie-crm:$VERSION_LABEL pie/crm
docker build -t instituutnederlandsetaal/taggers-dockerized-pie-gysseling:$VERSION_LABEL pie/gysseling

# Huggingface 
# Require local building
# docker build -t instituutnederlandsetaal/taggers-dockerized-huggingface-base:$VERSION_LABEL huggingface/base
# docker build -t instituutnederlandsetaal/taggers-dockerized-huggingface-tdn:$VERSION_LABEL huggingface/tdn
