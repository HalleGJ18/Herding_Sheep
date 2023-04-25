import pandas as pd
import numpy as np

SHEEP_CSV = "sheep_data5.csv"
DOG_CSV = "dog_data5.csv"

sheep_data = pd.read_csv(SHEEP_CSV, sep="|", index_col=0)
dog_data = pd.read_csv(DOG_CSV, sep="|", index_col=0)

sheep_data.rename(columns={'X_Positions':'sheep_x_positions', 'Y_Positions':'sheep_y_positions'}, inplace=True)
dog_data.rename(columns={'X_Positions':'dog_x_positions', 'Y_Positions':'dog_y_positions'}, inplace=True)

print(sheep_data)
print(dog_data)

result = pd.merge(sheep_data, dog_data, left_index=True, right_index=True)

print(result)

result.to_csv("data5.csv", encoding='utf-8', sep="|")