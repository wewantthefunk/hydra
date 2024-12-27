#!/bin/bash

source hydra-env/bin/activate

if [ -f nohup.out ]; then
  rm nohup.out
fi

if [ -f test_data/test.db ]; then
  rm test_data/test.db
fi

nohup python app.py test_data/test.db &

python_pid=$(echo $!)

echo $python_pid

# setup the test data
python test/datasetup.py

# run the tests
python test/index.py

kill $python_pid

