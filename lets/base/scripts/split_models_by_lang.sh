curl -O http://www.ccl.kuleuven.be/~jonas/lets-1.0.0/lets_models-1.0.0-py3-none-any.zip

cp lets_models-1.0.0-py3-none-any.zip lets_models-1.0.0-nl.zip 
# strip all non-nl files
zip -d lets_models-1.0.0-nl.zip \
 lets_models-1.0.0.dist-info/\* \
 \*.de \
 \*.fr \
 \*.en \
 lets/models/tokenizer/de/\* \
 lets/models/tokenizer/en/\*\
 lets/models/tokenizer/fr/\* \

cp lets_models-1.0.0-py3-none-any.zip lets_models-1.0.0-fr.zip 
# strip all non-fr files
zip -d lets_models-1.0.0-fr.zip \
 lets_models-1.0.0.dist-info/\* \
 \*.de \
 \*.nl \
 \*.en \
 lets/models/tokenizer/de/\* \
 lets/models/tokenizer/en/\*\
 lets/models/tokenizer/nl/\* \

cp lets_models-1.0.0-py3-none-any.zip lets_models-1.0.0-de.zip 
# strip all non-de files
zip -d lets_models-1.0.0-de.zip \
 lets_models-1.0.0.dist-info/\* \
 \*.fr \
 \*.nl \
 \*.en \
 lets/models/tokenizer/fr/\* \
 lets/models/tokenizer/en/\*\
 lets/models/tokenizer/nl/\* \

 cp lets_models-1.0.0-py3-none-any.zip lets_models-1.0.0-en.zip 
# strip all non-en files
zip -d lets_models-1.0.0-en.zip \
 lets_models-1.0.0.dist-info/\* \
 \*.fr \
 \*.nl \
 \*.de \
 lets/models/tokenizer/fr/\* \
 lets/models/tokenizer/de/\*\
 lets/models/tokenizer/nl/\* \

 rm lets_models-1.0.0-py3-none-any.zip