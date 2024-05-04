from database import PlayStationBD
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class GraphCreator:
    def __init__(self):
        self.db = PlayStationBD()
        self.df = self.db.data_manage()
        self.genre_list = self.db.unique_genre()

    # Statistic part
    def create_distribution_graph(self, attribute):
        plt.figure(figsize=(8, 6))
        sns.histplot(self.df[attribute], kde=True)
        plt.title(f"Distribution of {attribute}")
        plt.xlabel(attribute)
        plt.ylabel("Frequency")
        plt.grid(True)
        # plt.show()
        return plt.gcf()

    def create_pie_chart(self):
        pass

    def create_line_graph(self):
        pass

    def create_bar_plot(self):
        pass

    def create_scatter_plot(self):
        pass

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
        action_games = self.df[self.df['Genre'] == 'Action'].copy()

        publisher_stats = action_games.groupby('Publisher').agg(
            {'OriginalPrice(THB)': 'mean', 'Rating': 'mean', 'Title': 'count'}).reset_index()
        publisher_stats.rename(columns={'Title': 'GameCount'}, inplace=True)

        # Select top 20 publishers by game count
        top_publishers = publisher_stats.nlargest(20, 'GameCount')

        # Filter action_games by top publishers
        action_games_top_publishers = action_games[action_games['Publisher'].isin(top_publishers['Publisher'])].copy()

        # Calculate z-scores for OriginalPrice and Rating
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

        # Define threshold for outliers (e.g., 3 standard deviations from the mean)
        outlier_threshold = 3

        # Remove outliers
        action_games_no_outliers = action_games_top_publishers[
            (np.abs(action_games_top_publishers['OriginalPrice_zscore']) <= outlier_threshold) & (
                    np.abs(action_games_top_publishers['Rating_zscore']) <= outlier_threshold)].copy()

        # Plot scatter plot without outliers
        plt.figure(figsize=(8, 5))
        sns.scatterplot(data=action_games_no_outliers, x='OriginalPrice(THB)', y='Rating', hue='Publisher', alpha=0.7,
                        s=150)

        # Add labels and title
        plt.title('Original Price vs. Rating by Top 20 Publishers for Action Games')
        plt.xlabel('Original Price (THB)')
        plt.ylabel('Rating')
        legend = plt.legend(title='Publisher', loc='upper left', bbox_to_anchor=(1, 1))
        legend.get_title().set_fontsize('10')  # Set the font size of the legend title
        for text in legend.get_texts():
            text.set_fontsize('8')  # Set the font size of the legend labels

        plt.grid(True)
        # plt.show()
        return plt.gcf()


# # Example usage:
# if __name__ == "__main__":
#     graph_creator = GraphCreator()
#     graph_creator.create_distribution_graph('Discount(%)')  # Example of creating a distribution graph
