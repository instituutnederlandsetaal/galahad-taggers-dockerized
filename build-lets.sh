# Set the default label
: ${VERSION_LABEL:=dev}

echo "Will build taggers with version <$VERSION_LABEL>. Set VERSION_LABEL to override this."

# Base images
docker build -t instituutnederlandsetaal/taggers-dockerized-base:$VERSION_LABEL base


# LETS languages
docker build -t instituutnederlandsetaal/taggers-dockerized-lets-nl:$VERSION_LABEL --build-arg LETS_LANG=nl lets/base
docker build -t instituutnederlandsetaal/taggers-dockerized-lets-de:$VERSION_LABEL --build-arg LETS_LANG=de lets/base
docker build -t instituutnederlandsetaal/taggers-dockerized-lets-fr:$VERSION_LABEL --build-arg LETS_LANG=fr lets/base
docker build -t instituutnederlandsetaal/taggers-dockerized-lets-en:$VERSION_LABEL --build-arg LETS_LANG=en lets/base