import pandas as pd

dfPokemon = pd.read_csv('dataPokemon.csv')

print(dfPokemon.describe().drop(['#','Generation'],axis=1).columns)