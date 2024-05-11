import re
import pandas as pd


class PlayStationDB:
    def __init__(self):
        self.df = pd.read_csv('historic_deals.csv')
        self.df.dropna(inplace=True)
        self.new_df = self.df.copy()

    def data_manage(self):
        # Title
        self.new_df['Edition'] = self.new_df['Title'].str.extract(r'\((.*?)\)')
        self.new_df['Title'] = self.new_df['Title'].apply(lambda x: re.sub(r'\((.*?)\)', '', x))

        # DiscountPCT
        self.new_df.rename(columns={'DiscountPCT': 'Discount(%)'}, inplace=True)
        self.new_df['Discount(%)'] = self.new_df['Discount(%)'].apply(lambda x: x.replace('%', '') if '%' in x else x)
        self.new_df = self.new_df.drop(self.new_df[self.new_df['Discount(%)'] == 'Trial'].index)
        self.new_df['Discount(%)'] = self.new_df['Discount(%)'].astype(int)

        # Original Price (Baht)
        self.new_df.rename(columns={'OriginalPrice': 'OriginalPrice(THB)'}, inplace=True)
        self.new_df['OriginalPrice(THB)'] = self.new_df['OriginalPrice(THB)'].apply(lambda x: x[3:])
        self.new_df['OriginalPrice(THB)'] = self.new_df['OriginalPrice(THB)'].apply(
            lambda x: x.replace(',', '') if ',' in x else x)
        self.new_df['OriginalPrice(THB)'] = self.new_df['OriginalPrice(THB)'].apply(
            lambda x: float(round(float(x) * 4.65)))


        # Discount Price (Baht)
        self.new_df.rename(columns={'DiscountPrice': 'DiscountPrice(THB)'}, inplace=True)
        self.new_df['DiscountPrice(THB)'] = self.new_df['DiscountPrice(THB)'].apply(lambda x: x[3:])
        self.new_df['DiscountPrice(THB)'] = self.new_df['DiscountPrice(THB)'].apply(
            lambda x: x.replace(',', '') if ',' in x else x)
        self.new_df['DiscountPrice(THB)'] = self.new_df['DiscountPrice(THB)'].apply(
            lambda x: float(round(float(x) * 4.65)))

        # Discount_endtime
        self.new_df['Discount_Endtime'] = self.new_df['Discount_Endtime'].apply(lambda x: x[:-4])
        self.new_df['Discount_Endtime'] = pd.to_datetime(self.new_df['Discount_Endtime'], format='%d/%m/%Y %I:%M %p')

        # Rating
        self.new_df['Rating'] = self.new_df['Rating'].apply(lambda x: x * 2)

        # Rating Count
        self.new_df['Rating_count'] = self.new_df['Rating_count'].apply(lambda x: x.replace('.', '') if '.' in x else x)
        self.new_df['Rating_count'] = self.new_df['Rating_count'].apply(
            lambda x: x.replace('k', '000') if 'k' in x else x)
        self.new_df['Rating_count'] = self.new_df['Rating_count'].apply(
            lambda x: x.replace('m', '000000') if 'm' in x else x)
        self.new_df['Rating_count'] = pd.to_numeric(self.new_df['Rating_count'].replace('No', pd.NaT), errors='coerce')
        self.new_df['Rating_count'] = self.new_df['Rating_count'].fillna(self.new_df['Rating_count'].median())

        self.new_df['Rating_count'] = self.new_df['Rating_count'].astype(int)

        # Genre
        pass

        # ReleaseDate
        self.new_df['ReleaseDate'] = pd.to_datetime(self.new_df['ReleaseDate'], format='%d/%m/%Y')

        self.new_df = self.new_df[
            ['Title', 'Edition', 'Publisher', 'Link', 'Discount(%)', 'OriginalPrice(THB)', 'DiscountPrice(THB)'
                , 'Discount_Endtime', 'Rating', 'Rating_count', 'Genre', 'ReleaseDate']]

        return self.new_df

    def unique_genre(self):
        combined_genres = self.new_df['Genre'].str.split(', ')
        unique_genres = set()
        for genres_list in combined_genres:
            unique_genres.update(genres_list)
        unique_genres = list(unique_genres)
        return unique_genres

    def without_outliners_IQR(self, attribute, df):
        Q1 = df[attribute].quantile(0.25)
        Q3 = df[attribute].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        new_new_df = df[(df[attribute] >= lower_bound) & (df[attribute] <= upper_bound)]
        return new_new_df

    def without_outliners_SD(self, attribute, df):
        mean = df[attribute].mean()
        std = df[attribute].std()

        lower_bound = mean - 1.5 * std
        upper_bound = mean + 1.5 * std

        new_new_df = df[(df[attribute] >= lower_bound)
                                 & (df[attribute] <= upper_bound)]
        return new_new_df





