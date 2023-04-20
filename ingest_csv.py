import pandas as pd
import numpy as np

sheep_df = pd.read_csv("sheep_data.csv", sep="|", index_col=0)
dog_df = pd.read_csv("dog_data.csv", sep="|", index_col=0)

print(sheep_df)
print(dog_df)
# print(dog_df.to_string())
