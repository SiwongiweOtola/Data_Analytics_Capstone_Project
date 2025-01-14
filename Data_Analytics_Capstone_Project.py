# -*- coding: utf-8 -*-
"""Siwongiwe_Data Analytics Capstone Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1t12eEdHPAC0O3Ev0eCiqds4AqdbbbITd

## Task 1: Data Loading (Python)

1. Read the csv file and load it into a pandas dataframe.
2. Display the first five rows of your dataframe.
3. Display the data types of the columns.
"""

## Import Libraries
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt
print ('Setup Completed')

## Read the csv file
airbnb_df = pd.read_csv('/content/sample_data/Airbnb_Open_Data[1].csv')
print ('File read and converted into dataframe')

from google.colab import drive
drive.mount('/content/drive')

## Display the first 5 rows
airbnb_df.head(5)

## Display the data types
airbnb_df.dtypes

"""## Task 2a: Data Cleaning (Any Tool)

1. Drop some of the unwanted columns. These include `host id`, `id`, `country` and `country code` from the dataset.
2. State the reason for not including these columns for your Data Analytics.

If using Python for this exercise, please include the code in the cells below. If using any other tool, please include screenshoots before and after the elimination of the columns.
"""

## Create list of columns to drop
columns_to_drop = ['host id', 'id', 'country', 'country code', 'lat', 'long', 'house_rules', 'license']

## Drop columns from dataframe and save in new dataframe
airbnb_dropped = airbnb_df.drop(columns_to_drop, axis=1)

airbnb_dropped.head(5)

"""The following columns are related, which are: Country, country code, latitude and longitude. This makes them to be not relevant to the analysis beacuse all the data is New York based Airbnb listings. The house rules are not relevant data  that is subected to the host or booking. All the spcaes for license are empty which makes the license column to be useless in the dataset. By removing non relevant columns thi will allow the dataset to be more concise for analysis purposes.

## Task 2b: Data Cleaning (Python)

- Check for missing values in the dataframe and display the count in ascending order. **If the values are missing, impute the values as per the datatype of the columns.**
- Check whether there are any duplicate values in the dataframe and, if present, remove them.
- Display the total number of records in the dataframe before and after removing the duplicates.
"""

## Check for missing values in the dataframe and display the count in ascending order.
missing_values = airbnb_dropped.isnull().sum().sort_values(ascending=True)

missing_values

#Impute missing values based on column data types # dtypes object or int or float
for column in airbnb_dropped.columns :
 if airbnb_dropped[column].dtype == 'object' :
    #Impute missing values with an empty string for object/string columns
    airbnb_dropped[column].fillna('',inplace=True)
else: #Impute missing values with the mean for numeric columns
    airbnb_dropped[column].fillna(airbnb_dropped[column].mean(), inplace=True)
    print('Missing values of objects replaced with empty string, and numerical values replace with mean of column.')

# Missing value recheck
missing_values = airbnb_dropped.isnull().sum().sort_values(ascending=True)
missing_values

# Output should be all 0

## Check whether there are any duplicate values in the dataframe and if present remove them.
duplicates = airbnb_dropped.duplicated().sum()
duplicates # Show duplicate records sum

# Remove duplicates
airbnb_dropped.drop_duplicates(inplace=True)
print('Duplicates removed')

## Display the total number of records in the dataframe after removing the duplicates.
final_records = len(airbnb_dropped)

final_records

"""## Task 3: Data Transformation (Any Tool)


- Rename the column `availability 365` to `days_booked`
- Convert all column names to lowercase and replace the spaces in the column names with an underscore "_".
- Remove the dollar sign and comma from the columns `price` and `service_fee`. If necessary, convert these two columns to the appropriate data type.

If using Python for this exercise, please include the code in the cells below. If using any other tool, please include screenshoots of your work.
"""

## Rename the column.
airbnb_dropped.rename(columns={'availability 365': 'days_booked'}, inplace=True)
print("Column renamed from 'availability 365'to 'days_booked'.")

## Convert all column names to lowercase and replace the spaces with an underscore "_"
airbnb_dropped.columns = airbnb_dropped.columns.str.lower().str.replace(' ','_')

# Check column names
column_names = airbnb_dropped.columns.tolist()
column_names

## Remove the dollar sign and comma from 'price' and 'service_fee' columns.
airbnb_dropped['price'] = airbnb_dropped['price'].str.replace(r'[$,]','', regex=True)
airbnb_dropped['service_fee'] = airbnb_dropped['service_fee'].str.replace(r'[$,]','',regex=True)

##convert 'price' and 'service_fee' columns to numeric data with float data type.
airbnb_dropped['price'] = pd.to_numeric(airbnb_dropped['price'], errors='coerce').astype(float)
airbnb_dropped['service_fee'] = pd.to_numeric(airbnb_dropped['service_fee'], errors='coerce').astype(float)

# Check values
airbnb_dropped.head(5)

"""### Task 4: Exploratory Data Analysis (Any Tool)

- List the count of various room types avaliable in the dataset.
- Which room type has the most strict cancellation policy?
- List the average price per neighborhood group, and highlight the most expensive neighborhood to rent from.

If using Python for this exercise, please include the code in the cells below. If using any other tool, please include screenshoots of your work.
"""

## List the count of various room types avaliable with Airbnb
room_type_counts = airbnb_dropped['room_type'].value_counts()
room_type_counts

## Which room type adheres to more strict cancellation policy
average_cancellation = airbnb_dropped.groupby('room_type')['cancellation_policy'].apply(lambda x: (x =='strict').mean())

room_type_most_strict = average_cancellation.idxmax()

room_type_most_strict

## List the average prices by neighbourhood, sort most expensive to least
airbnb_dropped['price'] = pd.to_numeric(airbnb_dropped['price'], errors='coerce')
average_price_neighbourhood = airbnb_dropped.groupby('neighbourhood')['price'].mean().sort_values(ascending=False)

average_price_neighbourhood

# Remove any empty values of neighbourhood group which might dispute the analysis later on
airbnb_clean = airbnb_dropped[(airbnb_dropped['neighbourhood_group'] !='') & (airbnb_dropped['neighbourhood'] !='')]

# List the average prices by neighbourhood group, sort most expensive to least
average_price_neighbourhood_group = airbnb_clean.groupby('neighbourhood_group')['price'].mean().sort_values(ascending=False)

average_price_neighbourhood_group

## Mention which is the most expensive neighborhood group for rentals
most_expensive_neighbourhood = average_price_neighbourhood.idxmax()
most_expensive_neighbourhood

## Get most expensive neighbourhood group
most_expensive_neighbourhood_group = average_price_neighbourhood_group.idxmax()
most_expensive_neighbourhood_group

"""## Task 5a: Data Visualization (Any Tool)

* List the count of various room types avaliable with Airnb
* Which room type adheres to more strict cancellation policy
* List the prices by neighborhood group and also mention which is the most expensive neighborhood group for rentals
* List the top 10 neighborhoods in the increasing order of their price with the help of a horizontal bar graph. Which is the cheapest neighborhood.
* List the neighborhoods which offer short term rentals within 10 days. Illustrate with a bar graph
* List the prices with respect to room type using a bar graph and also state your inferences.
* Create a pie chart that shows  distribution of booked days for each neighborhood group .Which neighborhood has the highest booking percentage.

If using Python for this exercise, please include the code in the cells below. If using any other tool, please include screenshoots of your work.
"""

# Top 10 most expensive neighbourhoods
top_10 = average_price_neighbourhood.head(10)
top_10

"""The answers for question 1-3 are the same as the ones in task 4, so question 1-3 has already been answered in the section above."""

# Display horizontal bar chart using seaborn
plt.figure(figsize=(10, 8))
plt.figure(figsize=(10, 6))
plt.barh(top_10.index, top_10.values, color='grey')

#Add Labels
plt.xlabel('Average Price ($)')
plt.ylabel('Neighbourhoods')
plt.title('Top 10 Most Expensive Neighbourhoods')
plt.gca().invert_yaxis() # Invert the y-axis to display the highest price at the top

# Add details
plt.xticks(rotation=45, ha='right')
plt.yticks(fontsize=10)
plt.grid(axis='x', linestyle='--')

# Add data labels to the bars
for index, value in enumerate(top_10.values):
  plt.text(value, index, f'${value:.2f}', va='center')

# Display Chart
plt.tight_layout()
plt.show()

# Display the 10 cheapest neighbourhoods
bottom_10 = average_price_neighbourhood.tail(10)
bottom_10

# Create the horizontal bar chart
plt.figure(figsize=(10, 6))
plt.barh(bottom_10.index, bottom_10.values,color='orange')

# Add data labels to the bars
for index, value in enumerate(bottom_10.values):
  plt.text(value, index, f'${value:.2f}', va='center')

# Display Chart
plt.tight_layout()
plt.show()

# Create a chart
plt.figure(figsize=(10, 6))
ax = sns.boxplot(x='room_type', y='price', data=airbnb_clean)
plt.xlabel('Room Type')
plt.ylabel('Price')
plt.title('Price Distribution of Listings by Room Type')
plt.xticks(rotation=45)

# Add label for median
medians = airbnb_clean.groupby('room_type')['price'].median()
room_types = airbnb_clean['room_type'].unique()

for xtick, label in enumerate(ax.get_xticklabels()):
  ax.text(xtick, medians[xtick] - 100,
          f"Median : ${medians[xtick]:.2f}",
          ha='center', va='top', fontsize=10)

plt.xticks(range(len(room_types)), room_types)  # Set custom x-tick labels
plt.tight_layout()
plt.show()

"""## Task 5b: Data Visualization (Any Tool)

* Does service price and room price have an impact on each other. Illustrate this relationship with a scatter plot and state your inferences
* Using a line graph show in which year the maximum construction of rooms took place.

If using Python for this exercise, please include the code in the cells below. If using any other tool, please include screenshoots of your work.
"""

# create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(airbnb_clean['service_fee'], airbnb_clean['price'], alpha=0.5)

# Add details
plt.xlabel('Service_Fee ($)')
plt.ylabel('Room Price ($)')
plt.title('Relationship between Service Fee and Room Price')

# Show chart
plt.tight_layout()
plt.show()

# Filter out rows where 'days_booked' is more than 0
filter_airbnb = airbnb_clean[(airbnb_clean['days_booked'] >= 0)]

# Calculate the average listings per year based on the difference between the current year and 'year_constructed'
current_year = pd.Timestamp.now().year
filter_airbnb['years_constructed'] = current_year - filter_airbnb['construction_year']
listings_per_year = filter_airbnb.groupby('years_constructed')['days_booked'].mean()

# Create the line chart
plt.figure(figsize=(10, 6))
plt.plot(listings_per_year.index, listings_per_year.values, marker='o', linestyle='-')

# Add labels
plt.xlabel('Year')
plt.ylabel('Total Listings')
plt.title('Total Listings Available per Year')
plt.xticks(listings_per_year.index, [f"{current_year - year}" for year in listings_per_year.index]) #show the year, instead of years from current
plt.gca().invert_xaxis()
plt.grid(True)

# Show the chart
plt.tight_layout()
plt.show()

"""## Task 5c: Data Visualization (Any Tool)

* With the help of box plots illustrate the following
 * Effect of Review Rate number on price
 * Effect of host identity verified on price

If using Python for this exercise, please include the code in the cells below. If using any other tool, please include screenshoots of your work.
"""

# Clean and group data for bar plot
# Remove rows with empty string value in 'host_identity_verified' column
verified_airbnb = airbnb_clean[airbnb_clean['host_identity_verified'].str.strip()!='']

# Map 'unconfirmed' to False and 'verified' to True in 'host_identity_verified' column
verified_airbnb['host_identity_verified'] = verified_airbnb['host_identity_verified'].map({'unconfirmed': False, 'verified':True})

# Group the data by 'rating' and 'host_identity_verified', and count the occurrences
verification_counts = verified_airbnb.groupby(['review_rate_number', 'host_identity_verified']).size().unstack()

# Create the bar plot
verification_counts.plot(kind='bar', stacked=False, figsize=(10, 6))
plt.xlabel('Rating')
plt.ylabel('Number of Hosts')
plt.title('Number of Verified and Unverified Hosts for Each Rating')
plt.legend(title='Host Verification', labels=['Unverified', 'Verified'])
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Are verified host generally more expensive?
# Create a box plot or violin plot to compare prices for verified and unverified users
plt.figure(figsize=(10, 6))
ax = sns.violinplot(x='host_identity_verified', y='price', data=verified_airbnb)
plt.xlabel('Host Identity Verified')
plt.ylabel('Price')
plt.title('Price Distribution for Verified and Unverified Users')
plt.xticks([0, 1], ['Unverified', 'Verified'])

# Add labels for median and interquartile ranges
medians = verified_airbnb.groupby('host_identity_verified')['price'].median()
q1 = verified_airbnb.groupby('host_identity_verified')['price'].quantile(0.25)
q3 = verified_airbnb.groupby('host_identity_verified')['price'].quantile(0.75)

for xtick, label in enumerate(ax.get_xticklabels()):
  ax.annotate(f"Median: ${medians[xtick]:.2f}", (xtick, medians[xtick]),
              xytext=(5, 5), textcoords
              ='offset points', ha='center', va='bottom', fontsize=10)
  ax.annotate(f"IQR: ${q1[xtick]:.2f}-${q3[xtick]:.2f}", (xtick, q3[xtick]),
              xytext=(5, -110), textcoords='offset points', ha='center', va='bottom',
              fontsize=10)

plt.tight_layout()
plt.show()