
# Imports:
import pandas as pd
import numpy as np
import folium

# Import Csv file
deposits = pd.read_csv("/Users/Balfe/PycharmProjects/UCD Exercises/venv/database.csv")

# Initial analysis
print(deposits .info())
print(deposits.describe())
print(deposits.shape)
print(deposits.head(5))
print(deposits.tail(5))
print(deposits.columns)
print(deposits.index)


# Clean-up
missing_values_count = deposits.isnull().sum()
print(missing_values_count[0:20])

clean_deposits = deposits.fillna(0)
missing_values_count = clean_deposits.isnull().sum()
print(missing_values_count[0:20])

# deposits.drop(columns=["Institution Name"],axis=1,inplace=True)


# New Column
# clean_deposits["Avg_deposits"]=clean_deposits.assign(avg=clean_deposits.iloc[:,14:21].mean(axis=1))

# print(clean_deposits)

# Subsetting
Large_deposits = clean_deposits[clean_deposits["2016 Deposits"] > 1000000]


Is_NYC = clean_deposits["City"] == "New York City"
Is_NYC_or_LA_or_CH = clean_deposits["City"].isin(["New York City", "Los Angeles", "Chicago"])
Is_Large = clean_deposits["2016 Deposits"] > 1000000

NYC_Large = deposits[Is_Large & Is_NYC]
Multi_Large = deposits[Is_Large & Is_NYC_or_LA_or_CH]
print(Multi_Large)

Large_deposits.loc[:, 'Marker'] = Large_deposits["Branch Name"] + ' ' + Large_deposits["2016 Deposits"]\
   .map('${:,.0f}'.format)


# Map marking citys with deposits > 1m
Chase_map = folium.Map(
    location=[40, -99],
    tiles="OpenStreetMap",
    zoom_start=5)

for index, row in Large_deposits.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=row['Marker'],
                  icon=folium.map.Icon(icon='usd')).add_to(Chase_map)

Chase_map.save('map.html')
