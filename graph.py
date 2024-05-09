import pandas as pd

from database import PlayStationBD
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class GraphCreator:
    def __init__(self):
        self.db = PlayStationBD()
        self.df = self.db.data_manage()
        self.genre_list = self.db.unique_genre()
        self.rating_count = self.db.rating_count_without_outliners()

    # Statistic part
    def create_distribution_graph(self, attribute):
        plt.figure(figsize=(8, 6))
        if attribute == 'Rating_count':
            plt.ylim(0, 800)
            sns.histplot(self.rating_count[attribute], kde=True)
        else:
            sns.histplot(self.df[attribute], kde=True)
        plt.title(f"Distribution of {attribute}")
        plt.xlabel(attribute)
        plt.ylabel("Frequency")
        plt.grid(True)

        return plt.gcf()

    # def create_pie_chart(self, attribute):
    #     counts = self.df[self.genre_list].value_counts()
    #     plt.figure(figsize=(8, 6))
    #     plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140)
    #     plt.title(f"Pie Chart of {attribute}")
    #     return plt.gcf()
    def create_pie_chart(self, attribute):
        if attribute == 'Genre':
            # Count occurrences of each genre
            counts = pd.Series(np.zeros(len(self.genre_list)), index=self.genre_list)
            for genre in self.genre_list:
                counts[genre] = self.df['Genre'].str.contains(genre).sum()
        else:
            # For other attributes, use value_counts directly
            counts = self.df[attribute].value_counts()

        counts = counts.sort_values(ascending=False)
        plt.figure(figsize=(8, 6))
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140)
        plt.title(f"Pie Chart of {attribute}")
        return plt.gcf()

    # def create_line_graph(self):
    #     pass
    #
    # def create_bar_plot(self):
    #     pass
    #
    # def create_scatter_plot(self):
    #     pass

    # Data Storytelling Part
    # def create_distribution_graph(self):
    #     pass
    #
    # def create_correlation_graph(self):
    #     pass
    #
    # def create_bar_plot(self):
    #     pass
    #
    # def create_line_genre_year(self):
    #     pass

    def create_scatter_plot_originalprice_rating(self):
        actions = self.df[self.df['Genre'] == 'Action'].copy()

        publisher_stats = actions.groupby('Publisher').agg(
            {'OriginalPrice(THB)': 'mean', 'Rating': 'mean', 'Title': 'count'}).reset_index()
        publisher_stats.rename(columns={'Title': 'GameCount'}, inplace=True)

        top_publishers = publisher_stats.nlargest(20, 'GameCount')

        action_games_top_publishers = actions[actions['Publisher'].isin(top_publishers['Publisher'])].copy()

        action_games_top_publishers.loc[:, 'OriginalPrice_zscore'] = (
                                                                             action_games_top_publishers[
                                                                                 'OriginalPrice(THB)'] -
                                                                             action_games_top_publishers[
                                                                                 'OriginalPrice(THB)'].mean()) / \
                                                                     action_games_top_publishers[
                                                                         'OriginalPrice(THB)'].std()
        action_games_top_publishers.loc[:, 'Rating_zscore'] = (
                                                                      action_games_top_publishers['Rating'] -
                                                                      action_games_top_publishers['Rating'].mean()) / \
                                                              action_games_top_publishers['Rating'].std()

        outlier_threshold = 3

        # Remove outliers
        action_games_no_outliers = action_games_top_publishers[
            (np.abs(action_games_top_publishers['OriginalPrice_zscore']) <= outlier_threshold) & (
                    np.abs(action_games_top_publishers['Rating_zscore']) <= outlier_threshold)].copy()

        # Plot scatter plot without outliers
        plt.figure(figsize=(8, 6))
        plt.subplots_adjust(left=0.1, right=0.7, top=0.9, bottom=0.1)
        sns.scatterplot(data=action_games_no_outliers, x='OriginalPrice(THB)', y='Rating', hue='Publisher', alpha=0.7,
                        s=150)

        # Add labels and title
        plt.title('Original Price vs. Rating by Top 20 Publishers for Action Games')
        plt.xlabel('Original Price (THB)')
        plt.ylabel('Rating')
        legend = plt.legend(title='Publisher', loc='upper left', bbox_to_anchor=(1, 1))
        legend.get_title().set_fontsize('9')  # Set the font size of the legend title
        for text in legend.get_texts():
            text.set_fontsize('7')  # Set the font size of the legend labels

        plt.grid(True)
        # plt.show()
        return plt.gcf()

    # def create_scatter_plot_originalprice_rating(self):
    #     actions = self.df[self.df['Genre'] == 'Action'].copy()
    #
    #     publisher_stats = actions.groupby('Publisher').agg(
    #         {'OriginalPrice(THB)': 'mean', 'Rating': 'mean', 'Title': 'count'}).reset_index()
    #     publisher_stats.rename(columns={'Title': 'GameCount'}, inplace=True)
    #
    #     top_publishers = publisher_stats.nlargest(20, 'GameCount')
    #
    #     action_games_top_publishers = actions[actions['Publisher'].isin(top_publishers['Publisher'])].copy()
    #
    # action_games_top_publishers.loc[:, 'OriginalPrice_zscore'] = ( action_games_top_publishers[ 'OriginalPrice(
    # THB)'] - action_games_top_publishers[ 'OriginalPrice(THB)'].mean()) / \ action_games_top_publishers[
    # 'OriginalPrice(THB)'].std() action_games_top_publishers.loc[:, 'Rating_zscore'] = (
    # action_games_top_publishers['Rating'] - action_games_top_publishers['Rating'].mean()) / \
    # action_games_top_publishers['Rating'].std()
    #
    #     # Calculate IQR for 'OriginalPrice(THB)' and 'Rating'
    #     Q1_price = action_games_top_publishers['OriginalPrice(THB)'].quantile(0.25)
    #     Q3_price = action_games_top_publishers['OriginalPrice(THB)'].quantile(0.75)
    #     IQR_price = Q3_price - Q1_price
    #
    #     Q1_rating = action_games_top_publishers['Rating'].quantile(0.25)
    #     Q3_rating = action_games_top_publishers['Rating'].quantile(0.75)
    #     IQR_rating = Q3_rating - Q1_rating
    #
    #     # Define outlier thresholds based on IQR
    #     outlier_threshold_price = 1.5 * IQR_price
    #     outlier_threshold_rating = 1.5 * IQR_rating
    #
    #     # Remove outliers
    #     action_games_no_outliers = action_games_top_publishers[
    #         (action_games_top_publishers['OriginalPrice(THB)'] >= Q1_price - outlier_threshold_price) &
    #         (action_games_top_publishers['OriginalPrice(THB)'] <= Q3_price + outlier_threshold_price) &
    #         (action_games_top_publishers['Rating'] >= Q1_rating - outlier_threshold_rating) &
    #         (action_games_top_publishers['Rating'] <= Q3_rating + outlier_threshold_rating)].copy()
    #
    #     # Plot scatter plot without outliers
    #     plt.figure(figsize=(8, 6))
    #     plt.subplots_adjust(left=0.1, right=0.6, top=0.9, bottom=0.1)
    #     sns.scatterplot(data=action_games_no_outliers, x='OriginalPrice(THB)', y='Rating', hue='Publisher', alpha=0.7,
    #                     s=150)
    #
    #     # Add labels and title
    #     plt.title('Original Price vs. Rating by Top 20 Publishers for Action Games')
    #     plt.xlabel('Original Price (THB)')
    #     plt.ylabel('Rating')
    #     legend = plt.legend(title='Publisher', loc='upper left', bbox_to_anchor=(1, 1))
    #     legend.get_title().set_fontsize('10')  # Set the font size of the legend title
    #     for text in legend.get_texts():
    #         text.set_fontsize('8')  # Set the font size of the legend labels
    #
    #     plt.grid(True)
    #     # plt.show()
    #     return plt.gcf()
    #
    #
