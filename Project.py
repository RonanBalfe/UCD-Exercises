import pandas as pd
import numpy as np

deposits = pd.read_csv("/Users/Balfe/PycharmProjects/UCD Exercises/venv/database.csv")

print(deposits.describe())
print(deposits.head(5))
print(deposits.tail(5))
print(deposits.shape)


missing_values_count = deposits.isnull().sum()
print(missing_values_count[0:20])

cleaned_deposits =deposits.fillna(0)
missing_values_count = cleaned_deposits.isnull().sum()
print(missing_values_count[0:20])



