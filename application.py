import tkinter as tk
from tkinter import ttk

import csv
import os
import copy
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas.plotting import scatter_matrix

from database import PlayStationBD
from graph import GraphCreator


class ApplicationUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PlayStation")
        # self.geometry('1600x1200')
        self.info_frame = tk.Frame()
        self.statistic_frame = tk.Frame()
        self.stat_graph_frame = tk.Frame(self.statistic_frame)
        self.stat_settings_frame = tk.Frame(self.statistic_frame)
        self.data_story_frame = tk.Frame()
        self.data_graph_frame = tk.Frame(self.data_story_frame)
        self.data_settings_frame = tk.Frame(self.data_story_frame)
        self.about_frame = tk.Frame()
        self.init_component()
        self.current_frame = tk.Frame()
        self.load_page('Info')

        self.DB = PlayStationBD()
        self.df = self.DB.data_manage()
        self.graph = GraphCreator()

    def init_component(self):
        # menu
        menu = tk.Menu(self)
        self.config(menu=menu)
        select_menu = tk.Menu(menu)
        menu.add_cascade(label='Menu', menu=select_menu)
        select_menu.add_command(label="Info", command=lambda: self.load_page("Info"))
        select_menu.add_command(label="Statistic", command=lambda: self.load_page("Statistic"))
        select_menu.add_command(label="Data Storytelling", command=lambda: self.load_page("Data Storytelling"))
        select_menu.add_command(label="About", command=lambda: self.load_page("About"))
        select_menu.add_separator()
        select_menu.add_command(label="Exit", command=self.quit)

    def load_page(self, name_page):
        if name_page == "Info":
            self.create_info_page()
        elif name_page == "Statistic":
            self.create_statistic_page()
        elif name_page == "Data Storytelling":
            self.create_data_storytelling_page()
        elif name_page == "About":
            self.create_about_page()

    def change_frame(self, old_frame, new_frame):
        """ Change from one frame to another frame """
        # Change from one frame to another frame
        if old_frame != new_frame:
            old_frame.pack_forget()
            # old_frame.destroy()
            new_frame.pack()

        # Clear unused widgets
        if old_frame.winfo_children():
            for frame in old_frame.winfo_children():
                frame.grid_forget()

        plt.close('all')
        self.current_frame = new_frame

    # info page
    def create_info_page(self):
        self.change_frame(self.current_frame, self.info_frame)
        self.change_frame(self.stat_graph_frame, self.info_frame)

        tk.Label(self.info_frame, bg='black', fg='white', text='Info page is coming soon', height=20,
                 width=40).grid(column=0, row=0)

    # Statistic page
    def create_statistic_page(self):
        self.change_frame(self.current_frame, self.statistic_frame)
        self.change_frame(self.stat_graph_frame, self.statistic_frame)

        for widget in self.stat_settings_frame.winfo_children():
            # widget.destroy()
            widget.grid_forget()

        # generate graph zone
        self.att0 = tk.StringVar()
        self.att0.set('My graph')
        graph_text = tk.Label(self.stat_graph_frame, textvariable=self.att0)
        graph_text.grid(row=0, column=0, columnspan=2)

        show_my_graph = (tk.Label(self.stat_graph_frame, bg='white', fg='black', text='Statistic is coming soon',
                                  height=20, width=40).grid(row=1, column=0, columnspan=2))

        # setting zone
        text1 = tk.Label(self.stat_settings_frame, text="Select Graph:")
        text1.grid(row=0, column=0, columnspan=4)

        self.text_graph = tk.StringVar()
        select_graph_options = ['Histogram', 'Pie chart', 'Line graph', 'Scatterplot']
        select_graph = tk.OptionMenu(self.stat_settings_frame, self.text_graph, *select_graph_options)
        select_graph.grid(row=1, column=0, columnspan=4)

        text2 = tk.Label(self.stat_settings_frame, text="Attributes")
        text2.grid(row=3, column=0, columnspan=4)

        text3 = tk.Label(self.stat_settings_frame, text="X: ")
        text3.grid(row=4, column=0)

        self.att1 = tk.StringVar()
        attribute1_options = ['Discount(%)', 'OriginalPrice(THB)', 'DiscountPrice(THB)', 'Rating', 'Rating_count', 'Publisher', 'Genre']
        attribute2_options = ['Publisher', 'Genre']
        self.att1.set('')
        attribute1 = tk.OptionMenu(self.stat_settings_frame, self.att1, *attribute1_options)
        attribute1.grid(row=4, column=1)

        text4 = tk.Label(self.stat_settings_frame, text="Y: ")
        text4.grid(row=4, column=2)

        # self.att2 = tk.StringVar()
        # attribute2_options = ['Discount(%)', 'OriginalPrice(THB)', 'DiscountPrice(THB)', 'Rating', 'Rating_count']
        # self.att2.set('')
        # attribute2 = tk.OptionMenu(self.stat_settings_frame, self.att2, *attribute2_options)
        # attribute2.grid(row=4, column=3)

        show_button = ttk.Button(self.stat_settings_frame, text="Show", command=self.show_graph)
        show_button.grid(row=5, column=0, columnspan=4)

        reset_button = ttk.Button(self.stat_settings_frame, text="Reset", command=self.reset)
        reset_button.grid(row=6, column=0, columnspan=4)

        self.stat_graph_frame.grid(row=0, column=0)
        self.stat_settings_frame.grid(row=0, column=1)

    def get_graph_attributes(self):
        pass

    def show_graph(self):
        graph_type = self.text_graph.get()
        attribute1 = self.att1.get()
        # attribute2 = self.att2.get()

        if graph_type == 'Histogram':
            x = self.graph.create_distribution_graph(attribute1)
            dis = FigureCanvasTkAgg(x, master=self.stat_graph_frame)
            dis.draw()
            self.stat_graph_frame.grid_forget()
            dis.get_tk_widget().grid(row=1, column=0, columnspan=2)
            self.stat_graph_frame.grid(row=0, column=0)
        elif graph_type == 'Pie chart':
            x = self.graph.create_pie_chart(attribute1)
            pie = FigureCanvasTkAgg(x, master=self.stat_graph_frame)
            pie.draw()
            self.stat_graph_frame.grid_forget()
            pie.get_tk_widget().grid(row=1, column=0, columnspan=2)
            self.stat_graph_frame.grid(row=0, column=0)
        elif graph_type == 'Scatterplot':
            x = self.graph.create_scatter_plot_originalprice_rating()
            sca = FigureCanvasTkAgg(x, master=self.stat_graph_frame)
            sca.draw()
            self.stat_graph_frame.grid_forget()
            sca.get_tk_widget().grid(row=1, column=0, columnspan=2)
            self.stat_graph_frame.grid(row=0, column=0)
        else:
            # self.DB.create_scatter_plot(attribute1, attribute2)
            pass

    def reset(self):
        self.att0.set('My Graph')
        self.text_graph.set(' ')
        self.att1.set(' ')
        # self.att2.set(' ')

        for widget in self.stat_graph_frame.winfo_children():
            widget.destroy()

        tk.Label(self.stat_graph_frame, textvariable=self.att0).grid(row=0, column=0, columnspan=2)
        tk.Label(self.stat_graph_frame, bg='white', fg='black', text='Statistic is coming soon',
                 height=20, width=40).grid(row=1, column=0, columnspan=2)

    # Data story
    def create_data_storytelling_page(self):
        self.change_frame(self.current_frame, self.data_story_frame)

        tk.Label(self.data_story_frame, bg='#ebd694', fg='black', text='Data Storytelling page is coming soon',
                 height=20,
                 width=40).grid(column=0, row=0)

        # self.att3 = tk.StringVar()
        # self.att3.set('Select Graph')
        # graph_selected = ttk.Combobox(self.data_graph_frame, textvariable=self.att3)
        # discriptive = tk.Frame()

    # about page
    def create_about_page(self):
        self.change_frame(self.current_frame, self.about_frame)

        # test_graph = tk.Frame(self.about_frame)
        # self.graph_text.grid(row=0, column=0, columnspan=2)
        tk.Label(self.about_frame, bg='#edabe4', fg='#690218', text='this is About page...', height=20,
                 width=40).grid(column=0, row=0)

    def run(self):
        self.mainloop()

# if __name__ == '__main__':
#     app = ApplicationUI()
#     app.run()
