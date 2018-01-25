import pandas as pd

df = pd.read_csv("data/tmdb_5000_credits.csv")
f = open("movies","w")

for i in range(len(df["title"])):
    f.write(df["title"][i] + "\n")

f.close()