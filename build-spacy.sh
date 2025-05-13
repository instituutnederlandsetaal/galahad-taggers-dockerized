# Set the default label
: ${VERSION_LABEL:=1}

echo "Will build taggers with version <$VERSION_LABEL>. Set VERSION_LABEL to override this."

# Base image
docker build -t ccl-kuleuven/taggers-dockerized-base:$VERSION_LABEL base

#docker build -t instituutnederlandsetaal/taggers-dockerized-spacy-la-lg:$VERSION_LABEL spacy/latin
# Spacy languages
docker build -t ccl-kuleuven/taggers-dockerized-spacy-nl-lg:$VERSION_LABEL --build-arg SPACY_MODEL=nl_core_news_lg --build-arg TAG=$VERSION_LABEL spacy/base
docker build -t ccl-kuleuven/taggers-dockerized-spacy-en-lg:$VERSION_LABEL --build-arg SPACY_MODEL=en_core_web_lg --build-arg TAG=$VERSION_LABEL spacy/base
docker build -t ccl-kuleuven/taggers-dockerized-spacy-de-lg:$VERSION_LABEL --build-arg SPACY_MODEL=de_core_news_lg --build-arg TAG=$VERSION_LABEL spacy/base
docker build -t ccl-kuleuven/taggers-dockerized-spacy-fr-lg:$VERSION_LABEL --build-arg SPACY_MODEL=fr_core_news_lg --build-arg TAG=$VERSION_LABEL spacy/base
