#!/bin/bash
# download wget with homebrew

PROJECT_ID=postal-parser

brew install wget
mkdir temp
cd temp
wget http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip
unzip trainingandtestdata.zip

rm trainingandtestdata.zip test*.csv

cd ..
python train_test_split.py

rm -rf temp

gsutil cp pyspark_sa_train_data.csv gs://${PROJECT_ID}/pyspark_nlp/data/training_data.csv
gsutil cp pyspark_sa_train_data.csv gs://${PROJECT_ID}/pyspark_nlp/data/test_data.csv
rm pyspark_sa_train_data.csv pyspark_sa_test_data.csv

# have a beautiful day :)

