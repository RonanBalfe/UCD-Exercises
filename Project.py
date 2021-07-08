
# Imports:
import folium as folium
import numpy as np
import pandas as pd
import folium

# Import Csv file
deposits1 = pd.read_csv("/Users/Balfe/PycharmProjects/UCD Exercises/venv/database.csv")
state_pops = pd.read_csv("/Users/Balfe/PycharmProjects/UCD Exercises/state_pops.csv")

# Initial analysis
print(deposits1.info())
print(deposits1.describe())
print(deposits1.shape)
print(deposits1.head(5))
print(deposits1.tail(5))
print(deposits1.columns)
print(deposits1.index)

# Clean-up
missing_values_count = deposits1.isnull().sum()
print(missing_values_count[0:20])

deposits1 = deposits1.fillna(0)
missing_values_count = deposits1.isnull().sum()
print(missing_values_count[0:20])

# Indexing, sorting
deposits1_ind = deposits1.set_index(["State"])
deposits1_ind.sort_index(level=["State"], ascending=[True])
print(deposits1_ind)
print(deposits1_ind.loc[["NY"]])

# Grouping
print(deposits1.pivot_table(values="2016 Deposits", index="City", columns="State", fill_value=0, margins=True))
print(deposits1.pivot_table(values="2016 Deposits", index="State", aggfunc=[np.mean, np.median]))

# Subsetting - create Large deposits subset dataframe
Large_deposits= deposits1[deposits1["2016 Deposits"] > 1000000]

# Subsetting - create subset dataframes for Large deposits in selected city groupings
Is_NYC = deposits1["City"] == "New York City"
Is_NYC_or_LA_or_CH = deposits1["City"].isin(["New York City", "Los Angeles", "Chicago"])
Is_Large = deposits1["2016 Deposits"] > 1000000
NYC_Large = deposits1[Is_Large & Is_NYC]
Multi_Large = deposits1[Is_Large & Is_NYC_or_LA_or_CH]
print(NYC_Large)
print(Multi_Large)

# Get aggregated deposit balances by state


# Join dataframes
# deposits2 = deposits1.merge(state_pops, on='State')

# print(deposits2.head(4))

# Map marking citys with deposits > 1m
Large_deposits.loc[:, 'Marker'] = Large_deposits["Branch Name"] + ' ' + Large_deposits["2016 Deposits"].map('${:,.0f}'.format)

Chase_map= folium.Map(location=[40, -99], tiles="OpenStreetMap", zoom_start=5)

for index, row in Large_deposits.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=row['Marker'],
                  icon=folium.map.Icon(icon='usd')).add_to(Chase_map)

Chase_map.save('map.html')
