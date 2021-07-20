

# Imports:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium


# Import Csv files
df_deposits = pd.read_csv("/Users/Balfe/PycharmProjects/UCD Exercises/venv/database.csv")
df_populations = pd.read_csv("/Users/Balfe/PycharmProjects/UCD Exercises/state_pops.csv")

# Initial analysis
print(df_deposits.columns)

# Clean-up - drop unwanted columns
df_deposits.drop(columns=['Institution Name', 'Branch Number', 'Established Date', 'Acquired Date', 'Street Address',
                          '2011 Deposits', '2012 Deposits', '2013 Deposits', '2014 Deposits', '2015 Deposits'],
                    axis=1, inplace=True)

# Clean-up - drop Head office as skews data
df_deposits.drop(df_deposits.loc[df_deposits['Main Office']==1].index, inplace=True)

#Analysis
print(df_deposits.columns)
print(df_deposits.info())
print(df_deposits.shape)

#Adjust Run display
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 2000)

# Replace Nulls with 0
missing_values_count = df_deposits.isnull().sum()
print(missing_values_count[0:10])

df_deposits = df_deposits.fillna(0)
missing_values_count = df_deposits.isnull().sum()
print(missing_values_count[0:10])

#Change 2010 Deposits column from Float to Integer
df_deposits['2010 Deposits'] = df_deposits['2010 Deposits'].astype(np.int64)
print(df_deposits.describe(include='int64'))

# Indexing, sorting
deposits_ind = df_deposits.set_index(["State"])
deposits_ind.sort_index(level=["State"], ascending=[True])
print(deposits_ind)
print(deposits_ind.loc[["NY"]])

# Subsetting - create Large deposits subset dataframe
df_large= df_deposits[df_deposits["2016 Deposits"] > 1000000]

# Subsetting - create subset dataframes for Large deposits in selected city groupings
Is_NYC = df_deposits["City"] == "New York City"
Is_NYC_or_LA_or_CH = df_deposits["City"].isin(["New York City", "Los Angeles", "Chicago"])
Is_Large = df_deposits["2016 Deposits"] > 1000000
NYC_Large = df_deposits[Is_Large & Is_NYC]
Multi_Large = df_deposits[Is_Large & Is_NYC_or_LA_or_CH]
print(NYC_Large)
print(Multi_Large)



# Grouping
df_pivot= pd.pivot_table(df_deposits,["2010 Deposits","2016 Deposits"], "State")

# Join dataframes
df_deposits2 = df_pivot.merge(df_populations, on='State')

# Looping,iterrows




#for row in deposits_ind[0]:
    #range = row[0]
    #row[0] =range
   # print(deposits_ind)

# Plotting
#Fig 1: Total deposits by State
ax= df_pivot.plot(alpha = 0.6, kind="bar", title= "Deposits by State")
ylab= ax.set_ylabel('Deposit total $', weight='bold', size=12)
xlab= ax.set_xlabel('US States', weight='bold', size=12)
for label in ax.get_xticklabels():
  label.set_rotation(45)
plt.show()

#Fig 2: 2016 Population by State
df_deposits2.plot(x="State", y="2016 Population", kind="bar", title= "State populations")
plt.show()


# Map marking citys with deposits > 1m
#df_large.loc[:, 'Marker'] = df_large["Branch Name"] + ' ' + df_large["2016 Deposits"].map('${:,.0f}'.format)

#Chase_map= folium.Map(location=[40, -99], tiles="OpenStreetMap", zoom_start=5)

#for index, row in df_large.iterrows():
    #folium.Marker([row['Latitude'], row['Longitude']], popup=row['Marker'],
                 # icon=folium.map.Icon(icon='usd')).add_to(Chase_map)

#Chase_map.save('map.html')