import pandas as pd

questions_pl= pd.read_csv('./data/polska.csv')

for x in range(questions_pl.__len__()):
    print(questions_pl.loc[x])