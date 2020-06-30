import pandas as pd
import numpy as np

cols = ['sentiment','id','date','query_string','user','text']
def main():
    df = pd.read_csv('temp/training.1600000.processed.noemoticon.csv', encoding = 'ISO-8859-1', names=cols)
    df = df.sample(frac=1).reset_index(drop=True) #Shuffle the data
    np.random.seed(42)
    mask = np.random.rand(len(df)) < 0.99
    train = df[mask].reset_index(drop=True)
    test = df[~mask].reset_index(drop=True)
    train.to_csv('pyspark_sa_train_data.csv')
    test.to_csv('pyspark_sa_test_data.csv')

if __name__=='__main__':
    main()

