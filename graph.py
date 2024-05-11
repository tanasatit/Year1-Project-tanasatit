import pandas as pd
from database import PlayStationDB
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class GraphCreator:
    def __init__(self):
        self.DB = PlayStationDB()
        self.df = self.DB.data_manage()
        self.genre_list = self.DB.unique_genre()
        self.rating_count = self.DB.without_outliners_IQR('Rating_count', self.df)
        self.action_df = self.df[self.df['Genre'] == 'Action'].copy()

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

    def create_pie_chart(self, attribute, bins=10):
        # Create bins for the attribute values
        bins_edges = np.linspace(self.df[attribute].min(), self.df[attribute].max(), bins + 1)
        labels = [f"{bins_edges[i]:.2f}-{bins_edges[i + 1]:.2f}" for i in range(len(bins_edges) - 1)]
        binned_values = pd.cut(self.df[attribute], bins=bins_edges, labels=labels, include_lowest=True)

        # Count the occurrences of each bin
        counts = binned_values.value_counts()
        counts = counts.sort_index()

        # Create the pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140)
        plt.title(f"Pie Chart of {attribute}")

        return plt.gcf()

    def create_line_graph(self, attribute1, attribute2):
        grouped_data = self.df.groupby(self.df['ReleaseDate'].dt.year)[[attribute1, attribute2]].mean()

        # Plot the line graph
        plt.figure(figsize=(8, 6))
        plt.plot(grouped_data.index, grouped_data[attribute1], label=attribute1)
        plt.plot(grouped_data.index, grouped_data[attribute2], label=attribute2)

        # Add labels and title
        plt.xlabel('Year')
        plt.ylabel('Average Value')
        plt.title('Line Graph of {} and {} Over Time'.format(attribute1, attribute2))
        plt.legend()
        plt.grid(True)
        # plt.show()

        return plt.gcf()

    def create_scatter_plot(self, attribute1, attribute2):
        # Create a scatter plot using seaborn
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=self.df, x=attribute1, y=attribute2)
        plt.title(f"Scatter Plot of {attribute1} vs {attribute2}")
        plt.xlabel(attribute1)
        plt.ylabel(attribute2)
        plt.grid(True)
        # plt.show()
        return plt.gcf()

    # Data Storytelling Part
    def create_action_distribution_graph(self):
        plt.figure(figsize=(8, 6))
        sns.histplot(self.action_df['OriginalPrice(THB)'], kde=True, alpha=0.5, label='Original Price')
        sns.histplot(self.action_df['DiscountPrice(THB)'], kde=True, alpha=0.5, label='Discount Price')
        plt.title("Distribution of OriginalPrice and DiscountPrice of Action Game")
        plt.xlabel("Price (THB)")
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(True)

        return plt.gcf()

    def create_scatter_plot_originalprice_rating(self):
        publisher_stats = self.action_df.groupby('Publisher').agg(
            {'OriginalPrice(THB)': 'mean', 'Rating': 'mean', 'Title': 'count'}).reset_index()
        publisher_stats.rename(columns={'Title': 'GameCount'}, inplace=True)

        self.top_publishers = publisher_stats.nlargest(20, 'GameCount')

        top_action_games = self.action_df[self.action_df['Publisher'].isin(self.top_publishers['Publisher'])].copy()

        # Remove outliers using Standard Deviation method
        top_action_games = self.DB.without_outliners_SD('OriginalPrice(THB)', top_action_games)
        top_action_games = self.DB.without_outliners_SD('Rating', top_action_games)

        # Plot scatter plot without outliers
        plt.figure(figsize=(8, 6))
        plt.subplots_adjust(left=0.1, right=0.7, top=0.9, bottom=0.1)
        sns.scatterplot(data=top_action_games, x='OriginalPrice(THB)', y='Rating', hue='Publisher', alpha=0.7,
                        s=150)

        # Add labels and title
        plt.title('Original Price vs. Rating by Top 20 Publishers for Action Games')
        plt.xlabel('Original Price (THB)')
        plt.ylabel('Rating')
        legend = plt.legend(title='Publisher', loc='upper left', bbox_to_anchor=(1, 1))
        legend.get_title().set_fontsize('9')
        for text in legend.get_texts():
            text.set_fontsize('7')

        plt.grid(True)
        # plt.show()
        return plt.gcf()

    def create_bar_plot_graph(self):
        publisher_discount_avg = self.df.groupby('Publisher')['Discount(%)'].mean().reset_index()
        top_publishers = publisher_discount_avg.nlargest(20, 'Discount(%)')
        top_publishers_data = self.df[self.df['Publisher'].isin(top_publishers['Publisher'])]

        # Remove outliers using IQR method
        top_publishers_data = self.DB.without_outliners_IQR('Discount(%)', top_publishers_data)

        plt.figure(figsize=(8, 6))
        sns.barplot(data=top_publishers_data, x='Publisher', y='Discount(%)', hue='Publisher', palette='viridis',
                    legend=False)

        plt.title('Average Discount Percentages by Top 20 Publisher')
        plt.xlabel('Publisher')
        plt.ylabel('Average Discount Percentage')
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

        plt.tight_layout()  # Adjust layout to prevent overlapping labels
        # plt.show()
        return plt.gcf()

    def create_genre_line_graph(self):
        # Group the data by year and genre to count the frequency of each genre in each year
        genre_counts = self.df.groupby([self.df['ReleaseDate'].dt.year, 'Genre']).size().unstack(fill_value=0)

        # Plot the line graph
        plt.figure(figsize=(8, 6))
        plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
        for genre in self.genre_list:
            if genre in genre_counts.columns:
                plt.plot(genre_counts.index, genre_counts[genre], label=genre)

        # Add labels and title
        plt.xlabel('Release Year')
        plt.ylabel('Frequency')
        plt.title('Frequency of Each Genre Over the Years')
        legend = plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        for text in legend.get_texts():
            text.set_fontsize('7')  # Set the font size of the legend labels
        plt.grid(True)

        return plt.gcf()

