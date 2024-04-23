import csv
import os
import copy
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix


df = pd.read_csv('historic_deals.csv')
df.dropna(inplace=True)

new_df = df.copy()
# DiscountPCT
pass


# Original Price (Baht)
new_df.rename(columns={'OriginalPrice': 'OriginalPrice(THB)'}, inplace=True)
new_df['OriginalPrice(THB)'] = new_df['OriginalPrice(THB)'].apply(lambda x: x[3:])
new_df['OriginalPrice(THB)'] = new_df['OriginalPrice(THB)'].apply(lambda x: x.replace(',','') if ',' in x else x)
new_df['OriginalPrice(THB)'] = new_df['OriginalPrice(THB)'].apply(lambda x: float(round(float(x)*4.65)))


# Discount Price (Baht)
new_df.rename(columns={'DiscountPrice': 'DiscountPrice(THB)'}, inplace=True)
new_df['DiscountPrice(THB)'] = new_df['DiscountPrice(THB)'].apply(lambda x: x[3:])
new_df['DiscountPrice(THB)'] = new_df['DiscountPrice(THB)'].apply(lambda x: x.replace(',','') if ',' in x else x)
new_df['DiscountPrice(THB)'] = new_df['DiscountPrice(THB)'].apply(lambda x: float(round(float(x)*4.65)))


# Discount_endtime
new_df['Discount_Endtime'] = new_df['Discount_Endtime'].apply(lambda x: x[:-4])
new_df['Discount_Endtime'] = pd.to_datetime(new_df['Discount_Endtime'], format='%d/%m/%Y %I:%M %p')


# Rating
new_df['Rating'] = new_df['Rating'].apply(lambda x: round(x))


# Rating Count
new_df['Rating_count'] = new_df['Rating_count'].apply(lambda x: x.replace('.', '') if '.' in x else x)
new_df['Rating_count'] = new_df['Rating_count'].apply(lambda x: x.replace('k', '000') if 'k' in x else x)
new_df['Rating_count'] = new_df['Rating_count'].apply(lambda x: x.replace('m', '000000') if 'm' in x else x)

new_df['Rating_count'] = pd.to_numeric(new_df['Rating_count'].replace('No', pd.NaT), errors='coerce')
new_df['Rating_count'].fillna(new_df['Rating_count'].median(), inplace=True)
new_df['Rating_count'] = new_df['Rating_count'].astype(int)


# Genre
pass


# ReleaseDate
new_df['ReleaseDate'] = pd.to_datetime(new_df['ReleaseDate'], format='%d/%m/%Y')

print(new_df.head())
