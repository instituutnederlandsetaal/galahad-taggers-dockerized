# LeTs

In this repo you will find the Python version of LeTs (originally in Java) created by Yazzoom.

***Warning***: the structure of this repository has changed in such a way that LeTs can be installed easily as a pip package. The biggest change is that the actual lets code has moved to the subdirectory `lets`.

***Remark***: If you are working on the lt3 research servers and want to run lets without installing, go to section 4.





## 1 Installing LeTs

### 1.1 Install dependencies

If you are working on the lt3 research servers, lets is installed and you can run it directly (see 4) but if you still need to install it to use it in some python script start at section 1.1.1

#### Python 3.5 or higher
Python 3.5 or higher with `pip`.

#### CRF++-0.58
LeTs uses CRF++ which you can install from the source. First you need to install a compiler. Note that depending on your enviroment you might need to `sudo` some commands.

##### Install Compiler

##### Ubuntu
```
apt-get install gcc g++ python-dev
```
##### OSX
Install [Xcode](https://developer.apple.com/xcode/)

##### Install CRF++ and Python Binding
The crfpp install file (.tar.gz) can be found in this repo. It can be installed on Ubuntu and OSX in the same way:



```
tar xzvf CRF++-0.58.tar.gz
cd CRF++-0.58/
./configure
make
make install # you might have to use sudo for this
```

##### 1.1.1 Install CRF++ Python Bindings

Then install the python binding for crf++. When working in a virtualenv, be sure to activate it, before executing these lines.

***remark***: on the servers you can also find this directory under `/opt/lets/CRF++-0.58/python`. Make sure you execute the following commands in a virtualenv.

```
cd python
python setup.py build
python setup.py install

ldconfig # you might have to use sudo for this
```

### 1.2 Install LeTs as a pip package

Make sure to execute the steps below in your own python environment.

#### 1.2.1 Install LeTs models package
The models are too large to include in the repo. They can be found in a separate python package `lets-models`. If you have access to one of the LT3 research or webservers, you can find this package as a wheel file: `\opt\lets_models-1.0.0-py3-none-any.whl`. It can also be found on the share `vtc_backup` under `software/lets`. You can copy it to your system and install with:

```
pip install lets_models-1.0.0-py3-none-any.whl
```

#### 1.2.2 Install LeTs package
Install with:
```
pip install git+https://github.ugent.be/lt3/lets.git
```
This will fail if you didn't install `lets-models`.

Pip will install the dependency `sortedcontainers` as a pip package.

### 1.3 Install LeTs not as a pip package

If you dont want to install lets as a pip package (for example if you want to modify the lets code), you need to install one more dependency in your python environment `sortedcontainers`.

```pip install sortedcontainers```

Clone this repo. If necessary, copy the lets subfolder to the place where you want to use it or somewhere in your python path. Next copy the models directory into that lets folder. It can be found on the share `vtc_backup` in the dir `sofware/lets/models`.






## 2 Running LeTs

### 2.1 Commandline

This works only if you installed lets as a pip package.

To run the complete pipeline:
```
lets-preprocessor nl input.txt output.txt
```
You can also run each step seperately. There are 5 steps:
* `lets-tokenizer`
* `lets-postag`
* `lets-lemmatizer`
* `lets-chunker`
* `lets-ner`

Info on parameters can be shown by using the `h` flag:
```lets-tokenizer -h```

### 2.2 Import as a python module in your own code

If you did not install lets as a pip package, you need to make sure that the lets subdirectory in this repo (with the models directory copied into it) is somewhere in your python path.

```
from lets.preprocessor import PreProcessor

preprocessor = PreProcessor(l='nl')
input = ['Dit is zin 1.', 'Dit is zin 2']
output = preprocessor.process_lines(input)
```
Each of the 5 steps has docstring on the constructor.
Each of the 5 steps also inherits from `abstract_step.py` where there is also a docstring on the methods.
For more details on how to the individual steps from code, see `preprocessor.py`, `abstract_steps.py` and the files for each individual step, eg. `tokenizer.py`, ...






## 3 Lets code folder structure

### lets directory

The lets directory contains the 5 steps of the Preprocessor pipeline:

* `tokenizer.py`
* `postag.py`
* `lemmatizer.py`
* `chunker.py`
* `ner.py`

The lets directory also contains `preprocessor.py` which executes the complete pipeline.


### Models directory

The models directory contains all the models and config files. 
However, this is not embedded in the repo (because it is really big). More info in point 1.2.1, 1.3 and also `lt3/lets-models` github project.


### Test directory

Contains unittests and integrationtests.
`test/integrationtests/data` is too large to put in this git repo.
Can be found in the share `vtc_backup` in dir `software/lets/integrationtests/data`.

### Steps directories

The steps directories (`lemmatizer_steps`, ...) contains for some of the main steps the substeps.






## 4 Running LeTs on the LT3 servers without installing

LeTs should be installed as a global python package on all the servers. This means you can directly use the commands from section 2.1.







## 5 Building the lets package

Make sure `build` package is installed with pip. Now from the root directory of this repo, run

```python -m build```

Inside a newly created `dist` directory, you can find the lets package as a binary (wheel) and source distribution (tar).






## 6 Tests
When making modifications to LeTs, always run the tests:

```
python -m test.integrationtests.test_data
```

Before doing this, copy the `test/integrationtests/data` directory from the share to your lets project (see above in 3).
