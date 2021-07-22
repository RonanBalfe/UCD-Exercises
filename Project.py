# Imports packages:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import matplotlib.ticker as ticker
import folium

# Import csv files:
df_deposits = pd.read_csv("/Users/Balfe/PycharmProjects/UCD Exercises/venv/database.csv")
df_populations = pd.read_csv("/Users/Balfe/PycharmProjects/UCD Exercises/venv/2016_Pops.csv")

# Adjust Run display so more columns are visible:
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 3000)

# Initial analysis:
print(df_deposits.columns)

# Clean-up - drop unwanted columns
df_deposits.drop(columns=['Institution Name', 'Branch Number', 'Established Date', 'Acquired Date', 'Street Address',
                          '2011 Deposits', '2012 Deposits', '2014 Deposits', '2015 Deposits'],
                 axis=1, inplace=True)

# Clean-up - drop Main office and NYC Branch as they are outliers:
df_deposits.drop(df_deposits.loc[df_deposits['Main Office'] == 1].index, inplace=True)
df_deposits.drop(df_deposits.loc[df_deposits['Branch Name'] == 'Madison and 48th St Branch'].index, inplace=True)

# Secondary analysis:
print(df_deposits.columns)
print(df_deposits.info())
print(df_deposits.shape)

# Replace Nulls with 0
print(df_deposits.isnull().sum())
df_deposits = df_deposits.fillna(0)

# Change 2010 Deposits column from Float to Integer
df_deposits['2010 Deposits'] = df_deposits['2010 Deposits'].astype(np.int64)
print(df_deposits.describe(include='int64').T)

# Subsetting - create Large deposits subset dataframe
df_large = df_deposits.loc[df_deposits["2016 Deposits"] > 1000000, ("Branch Name", "2016 Deposits", "Latitude",
                                                                    "Longitude")]

# Map marking citys with deposits > 1m
df_large.loc[:, 'Marker'] = df_large["Branch Name"] + ' ' + df_large["2016 Deposits"].map('${:,.0f}'.format)
Chase_map = folium.Map(location=[40, -99], tiles="OpenStreetMap", zoom_start=5)
for index, row in df_large.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=row['Marker'],
                  icon=folium.map.Icon(icon='usd')).add_to(Chase_map)
Chase_map.save('map.html')

# Pivots
df_pivot = pd.pivot_table(df_deposits, ["2010 Deposits", "2013 Deposits", "2016 Deposits"], "State",
                          aggfunc={"2010 Deposits": np.sum, "2013 Deposits": np.sum, "2016 Deposits": np.sum})

# Looping,iterrows
for index, row in df_deposits.iterrows():
    df_deposits.loc[index, 'Movement since 2010'] = row['2016 Deposits'] - row['2010 Deposits']
print(df_deposits.head(20))

# Indexing, sorting
deposits_ind = df_deposits.set_index(["State"])
deposits_ind.sort_index(level=["State"], ascending=[True])
print(deposits_ind)
print(deposits_ind.loc[["CA"]])

# Subsetting - create subset dataframes for Large deposits in selected city groupings
Is_NYC = df_deposits["City"] == "New York City"
Is_NYC_or_LA_or_CH = df_deposits["City"].isin(["New York City", "Los Angeles", "Chicago"])
Is_Large = df_deposits["2016 Deposits"] > 1000000
NYC_Large = df_deposits[Is_Large & Is_NYC]
Multi_Large = df_deposits[Is_Large & Is_NYC_or_LA_or_CH]
print(NYC_Large)
print(Multi_Large)

# Dictionary
State_Names = [{'State': 'AZ', 'StateNames': 'Arizona'}, {'State': 'CA', 'StateNames': 'California'},
               {'State': 'CO', 'StateNames': 'Colarado'}, {'State': 'CT', 'StateNames': 'Connecticut'},
               {'State': 'DC', 'StateNames': 'D.C.'}, {'State': 'FL', 'StateNames': 'Florida'},
               {'State': 'GA', 'StateNames': 'Georgia'}, {'State': '''ID''', 'StateNames': '''Idaho'''},
               {'State': 'IL', 'StateNames': 'Illinois'}, {'State': 'IN', 'StateNames': 'Indiana'},
               {'State': 'KY', 'StateNames': 'Kentucky'}, {'State': 'LA', 'StateNames': 'Louisiana'},
               {'State': 'MA', 'StateNames': 'Massachusetts'}, {'State': 'MI', 'StateNames': 'Michigan'},
               {'State': 'NV', 'StateNames': 'Nevada'}, {'State': 'NJ', 'StateNames': 'New Jersey'},
               {'State': 'NY', 'StateNames': 'New York'}, {'State': 'OH', 'StateNames': 'Ohio'},
               {'State': 'OK', 'StateNames': 'Oklahoma'}, {'State': 'OR', 'StateNames': 'Oregon'},
               {'State': 'PA', 'StateNames': 'Pennsylvania'}, {'State': 'TX', 'StateNames': 'Texas'},
               {'State': 'UT', 'StateNames': 'Utah'}, {'State': 'WA', 'StateNames': 'Washington'},
               {'State': 'WV', 'StateNames': 'West Virginia'}, {'State': 'WI', 'StateNames': ' Wisconsin'}]

df_StateNames = pd.DataFrame(data=State_Names)
print(df_StateNames.T)

# Join dataframes
df_deposits1 = df_pivot.merge(df_StateNames, on='State')
df_deposits2 = df_deposits1.merge(df_populations, on='StateNames')

# Function to create reusable code:


def sub(a, b):
    c = a-b
    return c


print(sub(df_deposits2['2016 Deposits'].sum(), df_deposits2['2010 Deposits'].sum()))
print(sub(df_deposits2['2016 Deposits'].sum(), df_deposits2['2013 Deposits'].sum()))
print(sub(df_deposits2['2013 Deposits'].sum(), df_deposits2['2010 Deposits'].sum()))

# Plotting
# Fig 1: Total deposits by State
ax = df_pivot.plot(kind="bar", title="Deposits by State", color=["forestgreen", "steelblue", "chocolate"], alpha=0.9)
ylab = ax.set_ylabel('Deposit total ($mln)', weight='bold', size=12)
xlab = ax.set_xlabel('US States', weight='bold', size=12)
for label in ax.get_xticklabels():
    label.set_rotation(45)
scale_y = 1e6
ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))
ax.yaxis.set_major_formatter(ticks_y)
plt.locator_params(axis="y", nbins=25)
plt.show()

# Fig 2: 2016 Population by State
ax = df_deposits2.plot(x="State", y="2016 Population", kind="bar", title="2016 State populations",
                       color="darkgoldenrod", alpha=0.9)
ylab = ax.set_ylabel('Population (mln)', weight='bold', size=12)
xlab = ax.set_xlabel('US States', weight='bold', size=12)
for label in ax.get_xticklabels():
    label.set_rotation(45)
scale_y = 1e6
ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_y))
ax.yaxis.set_major_formatter(ticks_y)
plt.locator_params(axis="y", nbins=20)
plt.show()

# Grouping
print(df_deposits2.groupby("State")["2016 Deposits"].mean())

# JP Morgan Data from online API:
api_data = requests.get('https://www.alphavantage.co/query?function=OVERVIEW&symbol=JPM&apikey=93WPKVHEISL8FOW3')
parsed_data = api_data.json()
print(parsed_data)
