# Set the default label
: ${VERSION_LABEL:=dev}

echo "Will build taggers with version <$VERSION_LABEL>. Set VERSION_LABEL to override this."

./buildall.sh

# Base image
docker push instituutnederlandsetaal/taggers-dockerized-base:$VERSION_LABEL

# PIE
docker push instituutnederlandsetaal/taggers-dockerized-pie-base:$VERSION_LABEL
docker push instituutnederlandsetaal/taggers-dockerized-pie-bab:$VERSION_LABEL
docker push instituutnederlandsetaal/taggers-dockerized-pie-tdn:$VERSION_LABEL
docker push instituutnederlandsetaal/taggers-dockerized-pie-crm:$VERSION_LABEL
docker push instituutnederlandsetaal/taggers-dockerized-pie-gysseling:$VERSION_LABEL

# Huggingface
# docker push instituutnederlandsetaal/taggers-dockerized-huggingface-base:$VERSION_LABEL
# docker push instituutnederlandsetaal/taggers-dockerized-huggingface-tdn:$VERSION_LABEL
