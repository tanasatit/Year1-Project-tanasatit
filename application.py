import tkinter as tk
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datamanager import DataManager
from graph import GraphCreator


class ApplicationUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.graph = GraphCreator()
        self.data_manager = DataManager()
        self.title("PlayStation")
        self.info_frame = tk.Frame(bg='white')
        self.statistic_frame = tk.Frame(bg='white')
        self.stat_graph_frame = tk.Frame(self.statistic_frame, bg='white')
        self.stat_settings_frame = tk.Frame(self.statistic_frame)
        self.data_story_frame = tk.Frame(bg='white')
        self.data_graph_frame = tk.Frame(self.data_story_frame, bg='white')
        self.data_settings_frame = tk.Frame(self.data_story_frame, bg='white')
        self.init_component()
        self.current_frame = tk.Frame()
        self.load_page('Info')

    def init_component(self):
        # Set up menu
        menu = tk.Menu(self)
        self.config(menu=menu)
        select_menu = tk.Menu(menu)
        menu.add_cascade(label='Menu', menu=select_menu)
        select_menu.add_command(label="Info", command=lambda: self.load_page("Info"))
        select_menu.add_command(label="Statistic", command=lambda: self.load_page("Statistic"))
        select_menu.add_command(label="Data Storytelling", command=lambda: self.load_page("Data Storytelling"))
        select_menu.add_separator()
        select_menu.add_command(label="Exit", command=self.quit)

    def load_page(self, name_page):
        if name_page == "Info":
            self.create_info_page()
        elif name_page == "Statistic":
            self.create_statistic_page()
        elif name_page == "Data Storytelling":
            self.create_data_storytelling_page()

    def change_frame(self, old_frame, new_frame):
        """ Change from one frame to another frame """
        if old_frame != new_frame:
            old_frame.pack_forget()
            new_frame.pack()

        if old_frame.winfo_children():
            for frame in old_frame.winfo_children():
                frame.grid_forget()

        matplotlib.pyplot.close()
        self.current_frame = new_frame

    # Info page
    def create_info_page(self):
        self.change_frame(self.current_frame, self.info_frame)
        self.change_frame(self.stat_graph_frame, self.info_frame)

        new_df = self.data_manager.get_data()
        self.column_list = new_df.columns.tolist()

        # Initialize Treeview with the column names
        self.result_table = ttk.Treeview(self.info_frame, columns=self.column_list, show='headings')
        self.result_table.bind("<Double-1>", self.on_double_click)

        # Search label and entry
        tk.Label(self.info_frame, bg='white', fg='black', text='Search: ').grid(row=0, column=0, columnspan=2,
                                                                                sticky="e")
        self.entry_text = tk.StringVar()
        entry = tk.Entry(self.info_frame, textvariable=self.entry_text, width=50)
        entry.grid(row=0, column=2, columnspan=2, sticky="w")
        entry.bind('<Return>', self.get_search_result)

        # Sort frame
        lb1 = tk.LabelFrame(self.info_frame, text='Sort by', bg='white', fg='black')
        lb1.grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")

        # Column menu
        self.column_text = tk.StringVar()
        self.column_text.set('')
        column_menu = tk.OptionMenu(lb1, self.column_text, *self.column_list, command=self.update_value_menu)
        column_menu.config(fg='black')
        column_menu.grid(row=0, column=0, padx=5)

        # Value menu
        self.value_text = tk.StringVar()
        self.value_text_menu = tk.OptionMenu(lb1, self.value_text, [])
        self.value_text_menu.config(fg='black')
        self.value_text_menu.grid(row=0, column=1, padx=5)

        # Sort and clear buttons
        tk.Button(lb1, text='Sort', command=self.sort).grid(row=0, column=2, )
        tk.Button(lb1, text='Clear', command=self.clear).grid(row=0, column=3)

        # Add scrollbars
        scrollbar_y = tk.Scrollbar(self.info_frame, orient="vertical", command=self.result_table.yview)
        scrollbar_y.grid(row=2, column=4, sticky="ns")
        scrollbar_x = tk.Scrollbar(self.info_frame, orient="horizontal", command=self.result_table.xview)
        scrollbar_x.grid(row=3, column=0, columnspan=4, sticky="ew")
        self.result_table.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Set column widths
        for col in self.column_list:
            self.result_table.heading(col, text=col)
            if col == 'Title':
                self.result_table.column(col, width=160)
            else:
                self.result_table.column(col, width=100)

        self.result_table.grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")

    def get_search_result(self, event):
        self.data_manager.update_result_table(self.entry_text.get(), self.result_table)

    def update_value_menu(self, *args):
        if self.value_text != '':
            self.value_text.set(' ')
        value_list = self.data_manager.get_value_list(self.column_text.get())
        menu = self.value_text_menu['menu']
        menu.delete(0, 'end')
        for value in value_list:
            menu.add_command(label=value, command=tk._setit(self.value_text, value))

    def on_double_click(self, event):
        item = self.result_table.selection()[0]
        # Get the URL
        url = self.result_table.item(item, 'values')[0]
        event.widget.focus_set()

    def sort(self):
        att1 = self.column_text.get()
        att2 = self.value_text.get()
        self.data_manager.sort_and_update_result_table(att1, att2, self.result_table)

    def clear(self):
        self.entry_text.set('')
        self.column_text.set(' ')
        self.value_text.set(' ')
        self.data_manager.update_result_table('', self.result_table)

    # Statistic page
    def create_statistic_page(self):
        self.change_frame(self.current_frame, self.statistic_frame)
        self.change_frame(self.stat_graph_frame, self.statistic_frame)

        for widget in self.stat_settings_frame.winfo_children():
            # Clear widgets
            widget.grid_forget()

        # graph zone
        fig = Figure(figsize=(8, 6))
        fig.add_subplot()
        canvas = FigureCanvasTkAgg(fig, master=self.stat_graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, columnspan=2, sticky="news")

        # Setting zone
        text1 = tk.Label(self.stat_settings_frame, text="Select Graph:")
        text1.grid(row=0, column=0, columnspan=4, ipady=10)

        # select graph
        self.text_graph = tk.StringVar()
        select_graph_options = ['Histogram', 'Pie chart', 'Line graph', 'Scatterplot']
        select_graph = tk.OptionMenu(self.stat_settings_frame, self.text_graph, *select_graph_options,
                                     command=self.on_graph_select)
        select_graph.grid(row=1, column=0, columnspan=4, ipady=10)

        # select attributes
        text2 = tk.Label(self.stat_settings_frame, text="Attributes")
        text2.grid(row=3, column=0, columnspan=4, ipady=10)
        text3 = tk.Label(self.stat_settings_frame, text="X : ")
        text3.grid(row=4, column=0, ipadx=5, ipady=10)

        self.att1 = tk.StringVar()
        attribute1_options = ['Discount(%)', 'OriginalPrice(THB)', 'DiscountPrice(THB)', 'Rating', 'Rating_count']
        self.att1.set('')
        attribute1 = tk.OptionMenu(self.stat_settings_frame, self.att1, *attribute1_options)
        attribute1.grid(row=4, column=1, ipadx=5, ipady=10)

        self.attribute2_label = tk.Label(self.stat_settings_frame, text="Y : ")

        self.att2 = tk.StringVar()
        attribute2_options = ['Discount(%)', 'OriginalPrice(THB)', 'DiscountPrice(THB)', 'Rating', 'Rating_count']
        self.att2.set('')
        self.attribute2_menu = tk.OptionMenu(self.stat_settings_frame, self.att2, *attribute2_options)

        # Show button
        show_button = ttk.Button(self.stat_settings_frame, text="Show", command=self.show_statistic_graph)
        show_button.grid(row=6, column=0, columnspan=4, ipady=10)

        # Reset button
        reset_button = ttk.Button(self.stat_settings_frame, text="Reset", command=self.reset)
        reset_button.grid(row=7, column=0, columnspan=4, pady=10)

        self.update_idletasks()
        self.stat_graph_frame.grid(row=0, column=0)
        self.stat_settings_frame.grid(row=0, column=1)

    def on_graph_select(self, event):
        if self.text_graph.get() in ['Line graph', 'Scatterplot']:
            self.attribute2_label.grid(row=5, column=0, ipadx=5, ipady=10)
            self.attribute2_menu.grid(row=5, column=1, ipadx=5, ipady=10)
        else:
            self.attribute2_label.grid_forget()
            self.attribute2_menu.grid_forget()

    def show_statistic_graph(self):
        text_graph = self.text_graph.get()
        attribute1 = self.att1.get()
        attribute2 = self.att2.get()
        if text_graph != '' and attribute1 != '':
            self.stat_graph_frame.grid_forget()
            if text_graph == 'Histogram':
                x = self.graph.create_distribution_graph(attribute1)
                dis = FigureCanvasTkAgg(x, master=self.stat_graph_frame)
                dis.get_tk_widget().grid(row=0, column=0, columnspan=2)
            elif text_graph == 'Pie chart':
                x = self.graph.create_pie_chart(attribute1)
                pie = FigureCanvasTkAgg(x, master=self.stat_graph_frame)
                pie.get_tk_widget().grid(row=0, column=0, columnspan=2)
            elif text_graph == 'Line graph':
                if attribute2 != '':
                    x = self.graph.create_line_graph(attribute1, attribute2)
                    line = FigureCanvasTkAgg(x, master=self.stat_graph_frame)
                    line.get_tk_widget().grid(row=0, column=0, columnspan=2)
            elif text_graph == 'Scatterplot':
                if attribute2 != '':
                    x = self.graph.create_scatter_plot(attribute1, attribute2)
                    sca = FigureCanvasTkAgg(x, master=self.stat_graph_frame)
                    sca.get_tk_widget().grid(row=0, column=0, columnspan=2)
            self.stat_graph_frame.grid(row=0, column=0)

    def reset(self):
        self.text_graph.set(' ')
        self.att1.set(' ')
        self.att2.set(' ')

        for widget in self.stat_graph_frame.winfo_children():
            widget.destroy()
        self.attribute2_label.grid_forget()
        self.attribute2_menu.grid_forget()

        fig = Figure(figsize=(8, 6))
        fig.add_subplot()
        canvas = FigureCanvasTkAgg(fig, master=self.stat_graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, columnspan=2, sticky="news")

    # Data story
    def create_data_storytelling_page(self):
        self.change_frame(self.current_frame, self.data_story_frame)

        # Graph frame
        self.att4 = tk.StringVar()
        self.att4.set('Page 1')
        page_text = tk.Label(self.data_graph_frame, textvariable=self.att4, bg='white', fg='black')
        page_text.grid(row=0, column=0, columnspan=2)

        x = self.graph.create_action_distribution_graph()
        self.story_graph = FigureCanvasTkAgg(x, master=self.data_graph_frame)
        self.story_graph.get_tk_widget().grid(row=1, column=0, columnspan=2)
        self.data_graph_frame.grid(row=0, column=0)

        # Setting frame
        self.page = 1
        self.tree = self.create_descriptive_table()
        self.tree.grid(row=0, column=0, columnspan=4, sticky="news")

        self.description_text = tk.StringVar()
        self.description_text.set('     This graph visualizes price distributions for action \n'
                                  'games, showing original and discounted prices in Thai \n'
                                  'Baht. It provides insights into pricing dynamics and \n'
                                  'discount trends in the action game genre.')
        tk.Label(self.data_settings_frame, textvariable=self.description_text, height=20,
                 width=40, bg='white', fg='black').grid(row=1, column=0, columnspan=4)

        self.back_button = ttk.Button(self.data_settings_frame, text="Back", command=self.back_story_page)
        self.next_button = ttk.Button(self.data_settings_frame, text="Next", command=self.next_story_page)
        self.next_button.grid(row=2, column=2, columnspan=2, sticky="news")

        self.data_graph_frame.grid(row=0, column=0)
        self.data_settings_frame.grid(row=0, column=1)

    def next_story_page(self):
        if self.page < 4:
            self.page += 1
            if self.page == 4:
                self.next_button.grid_forget()
            if self.page == 2:
                self.back_button.grid(row=2, column=0, columnspan=2, sticky="news")
            self.change_story_graph()

    def back_story_page(self):
        if self.page > 1:
            self.page -= 1
            if self.page == 1:
                self.back_button.grid_forget()
            if self.page == 3:
                self.next_button.grid(row=2, column=2, columnspan=2, sticky="news")
            self.change_story_graph()

    def change_story_graph(self):
        matplotlib.pyplot.close()
        self.story_graph.get_tk_widget().grid_forget()
        self.tree.grid_forget()

        if self.page == 1:
            self.att4.set('Page 1')
            self.description_text.set('     This graph visualizes price distributions for action \n'
                                      'games, showing original and discounted prices in Thai \n'
                                      'Baht. It provides insights into pricing dynamics and \n'
                                      'discount trends in the action game genre.')

            x = self.graph.create_action_distribution_graph()
            self.story_graph = FigureCanvasTkAgg(x, master=self.data_graph_frame)
            self.story_graph.get_tk_widget().grid(row=1, column=0, columnspan=2)
            self.tree = self.create_descriptive_table()
        elif self.page == 2:
            self.att4.set('Page 2')
            self.description_text.set("This scatter plot summarizes how pricing affects \n"
                                      "customer ratings for top 20 action game publishers. \n"
                                      "It shows pricing's impact on satisfaction and \n"
                                      "competitiveness, aiding publishers in strategy.")

            x = self.graph.create_scatter_plot_originalprice_rating()
            self.story_graph = FigureCanvasTkAgg(x, master=self.data_graph_frame)
            self.story_graph.get_tk_widget().grid(row=1, column=0, columnspan=2)
            self.tree = self.create_descriptive_table()
        elif self.page == 3:
            self.att4.set('Page 3')
            self.description_text.set(('     This bar plot compares average discount percentages \n'
                                       'among the top 20 publishers. It helps publishers adjust \n'
                                       'pricing and promotional strategies based on competitors.'))

            x = self.graph.create_bar_plot_graph()
            self.story_graph = FigureCanvasTkAgg(x, master=self.data_graph_frame)
            self.story_graph.get_tk_widget().grid(row=1, column=0, columnspan=2)
            self.tree = self.create_descriptive_table()
        elif self.page == 4:
            self.att4.set('Page 4')
            self.description_text.set('     This graph tracks the frequency of game releases \n'
                                      'across genres over time. It offers insights into genre \n'
                                      'trends each year, aiding publishers in staying informed \n'
                                      'about emerging trends.')

            x = self.graph.create_genre_line_graph()
            self.story_graph = FigureCanvasTkAgg(x, master=self.data_graph_frame)
            self.story_graph.get_tk_widget().grid(row=1, column=0, columnspan=2)
            self.tree = self.create_descriptive_table()
        self.tree.grid(row=0, column=0, columnspan=4, sticky="news")

    def create_descriptive_table(self):
        if self.page == 1:
            self.att_list = ['OriginalPrice(THB)', 'DiscountPrice(THB)']
        elif self.page == 2:
            self.att_list = ['OriginalPrice(THB)', 'Rating']
        elif self.page == 3:
            self.att_list = ['Discount(%)', 'DiscountPrice(THB)']
        elif self.page == 4:
            self.att_list = ['OriginalPrice(THB)', 'DiscountPrice(THB)']
        descriptive_stats = self.data_manager.get_descriptive(self.att_list[0], self.att_list[1])
        tree = ttk.Treeview(self.data_settings_frame)
        # tree.grid(row=0, column=0, columnspan=4, sticky="news")

        tree["columns"] = ["Statistic", self.att_list[0], self.att_list[1]]
        tree["show"] = "headings"
        tree.heading("Statistic", text="Statistic")
        tree.heading(self.att_list[0], text=self.att_list[0])
        tree.heading(self.att_list[1], text=self.att_list[1])

        for index, row in descriptive_stats.iterrows():
            tree.insert("", "end", values=[index] + row.tolist())
        return tree

    def run(self):
        self.mainloop()
