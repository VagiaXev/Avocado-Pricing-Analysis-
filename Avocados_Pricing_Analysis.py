#import modules
import pandas as pd
import numpy as np
import plotly.express as px

#load the dataset
price_data = pd.read_csv("avocado_pricing_data.csv")
print("Avocados_Data:\n",price_data.head(10))

#check for missing data
print("Missing Data:\n",price_data.isna().sum())

#check data types
print("Data Types:\n",price_data.dtypes)

#convert date column to datetime format
price_data["Date"] = pd.to_datetime(price_data["Date"])
print("Data Types:\n",price_data.dtypes)

#rename some columns
price_data.columns = ['Order_ID', 'Date', 'Average Price', 'Total Volume', 'PLU 4046 sold',
       'PLU 4225 sold', 'PLU 4770 sold ', 'Total Bags', 'Small Bags', 'Large Bags', 'XLarge Bags',
       'Type', 'Year', 'Region']
columns_name = price_data.columns
print(columns_name)

#define duplicate data
duplicate_data = price_data[price_data.duplicated(keep=False)]
print(duplicate_data)

#outliers detection
outliers_detect = price_data.describe()[['Average Price', 'Total Volume', 'PLU 4046 sold',
       'PLU 4225 sold', 'PLU 4770 sold ', 'Total Bags', 'Small Bags', 'Large Bags', 'XLarge Bags']]
print(outliers_detect)

#data visualization for outliers detection
fig = px.box(price_data, y=price_data['Total Volume'])
fig.show()

#create a function to find outliers using IQR
def find_outliers_IQR(df):
       q1=df.quantile(0.25)
       q3=df.quantile(0.75)
       IQR=q3-q1
       outliers = df[((df<(q1-1.5*IQR)) | (df>(q3+1.5*IQR)))]
       return outliers

outliers = find_outliers_IQR(price_data['Total Volume'])

print('Number of outliers: '+ str(len(outliers)))
print('\nMax outlier value: '+ str(outliers.max()))
print('\nMin outlier value: '+ str(outliers.min()))

#handle outliers
def impute_outliers_IQR(df):

   q1=df.quantile(0.25)
   q3=df.quantile(0.75)
   IQR=q3-q1
   upper = df[~(df>(q3+1.5*IQR))].max()
   lower = df[~(df<(q1-1.5*IQR))].min()
   df = np.where(df > upper,
       df.mean(),
       np.where(
           df < lower,
           df.mean(),
           df
           )
       )
   return df

price_data['Total Volume'] = impute_outliers_IQR(price_data['Total Volume'])

print('\nTotal Volume Statistics:\n',price_data.describe()['Total Volume'])

#data visualization for outliers detection
fig = px.box(price_data, y=price_data['Total Volume'])
fig.show()

#export data as a csv file
price_data.to_csv('C:/Users/Nikos/PycharmProjects/FinalAssignment/avocado_prices.csv')

#export data as an excel file
price_data.to_csv('C:/Users/Nikos/PycharmProjects/FinalAssignment/avocado_prices.xlsx')