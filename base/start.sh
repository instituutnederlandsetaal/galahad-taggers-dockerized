#!/bin/sh

# start the webservice
python3 webservice.py &

# start the tagger worker
python3 tagger_worker.py
