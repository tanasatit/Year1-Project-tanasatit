import webbrowser
from database import PlayStationDB
import pandas as pd


class DataManager:
    def __init__(self):
        self.DB = PlayStationDB()
        self.df = self.DB.data_manage()
        self.new_df = self.df.drop(['Link'], axis=1)

    def get_data(self):
        return self.new_df

    def search_data(self, search_entry):
        """
        :param search_entry: a text variable from info page
        :return: data that have this text
        """
        if not search_entry.strip():
            return pd.DataFrame()  # Return an empty DataFrame if search_entry is empty

        title_search = self.new_df['Title'].str.contains(
            search_entry,
            case=False,
            na=False)

        edition_search = self.new_df['Edition'].str.contains(
            search_entry,
            case=False,
            na=False)

        discountPTC_search = self.new_df['Discount(%)'].astype(str).str.contains(
            search_entry,
            case=False,
            na=False)

        price_search = self.new_df['OriginalPrice(THB)'].astype(str).str.contains(
            search_entry,
            case=False,
            na=False)

        discount_search = self.new_df['DiscountPrice(THB)'].astype(str).str.contains(
            search_entry,
            case=False,
            na=False)

        rating_search = self.new_df['Rating'].astype(str).str.contains(
            search_entry,
            case=False,
            na=False)

        rating_count_search = self.new_df['Rating_count'].astype(str).str.contains(
            search_entry,
            case=False,
            na=False)

        genre_search = self.new_df['Genre'].str.contains(
            search_entry,
            case=False,
            na=False)

        # Combine all search conditions using logical OR (|)
        combined_search = (title_search | edition_search | discountPTC_search | price_search |
                           discount_search | rating_search | rating_count_search | genre_search)

        # Filter the DataFrame based on the combined search conditions
        search_results = self.new_df[combined_search]
        return search_results

    def update_result_table(self, search_entry, result_table):
        # Check if there are children before attempting to delete them
        children = result_table.get_children()
        if children:
            result_table.delete(*children)  # Use *children to unpack the list of children

        # If search_entry is empty, return without adding any rows to the table
        if not search_entry.strip():
            return

        # Get search results
        search_results = self.search_data(search_entry)

        # Insert search results into the table
        for index, row in search_results.iterrows():
            result_table.insert('', 'end', values=row.tolist())
        result_table.bind("<Double-1>", lambda event: self.open_website(result_table))

    def get_value_list(self, column_type):
        value_list = []

        if column_type in ['Title', 'Edition', 'Publisher']:
            value_list = ['A-Z', 'Z-A']
        elif column_type in ['Discount(%)', 'OriginalPrice(THB)', 'DiscountPrice(THB)', 'Rating', 'Rating_count']:
            value_list = ['Lowest to Highest', 'Highest to Lowest']
        elif column_type == 'Genre':
            value_list = self.DB.unique_genre()
        elif column_type in ['Discount_Endtime', 'ReleaseDate']:
            value_list = ['Newest to Oldest', 'Oldest to Newest']

        return value_list

    def sort_and_update_result_table(self, attribute1, attribute2, result_table):
        if attribute1 and attribute2:
            if attribute2 == 'Lowest to Highest':
                ascending = True
            else:
                ascending = False

            if attribute2 in ['Lowest to Highest', 'Highest to Lowest']:
                self.sorted_df = self.new_df.sort_values(by=attribute1, ascending=ascending)
            elif attribute2 == 'A-Z':
                self.sorted_df = self.new_df.sort_values(by=attribute1, ascending=True, key=lambda x: x.str.lower())
            elif attribute2 == 'Z-A':
                self.sorted_df = self.new_df.sort_values(by=attribute1, ascending=False, key=lambda x: x.str.lower())
            elif attribute2 == 'Newest to Oldest':
                self.sorted_df = self.new_df.sort_values(by=attribute1, ascending=False)
            elif attribute2 == 'Oldest to Newest':
                self.sorted_df = self.new_df.sort_values(by=attribute1, ascending=True)

            # Update the result table with the sorted data
            self.update_result_table_from_df(self.sorted_df, result_table)

    def update_result_table_from_df(self, df, result_table):
        # Clear the existing table
        children = result_table.get_children()
        if children:
            result_table.delete(*children)

        # Insert data from the DataFrame into the result table
        for index, row in df.iterrows():
            result_table.insert('', 'end', values=row.tolist())
        result_table.bind("<Double-1>", lambda event: self.open_website(result_table))

    def get_descriptive(self, attribute1, attribute2):
        new_df = self.df[[attribute1, attribute2]]
        return new_df.describe()

    def open_website(self, result_table):
        selected_item = result_table.selection()
        if selected_item:
            item_data = result_table.item(selected_item)['values']
            title = item_data[0]
            edition = item_data[1]
            # Get the link from the database
            link = self.get_link(title, edition)
            # Open the link in the default web browser
            if link:
                webbrowser.open_new(link)

    def get_link(self, title, edition):
        # if the title and edition combination is not in the database, return None
        if (title not in self.df['Title'].values) or (edition not in self.df['Edition'].values):
            return None
        else:
            # get the link from the DataFrame
            link = self.df.loc[(self.df['Title'] == title) & (self.df['Edition'] == edition), 'Link'].iloc[0]
            return link

