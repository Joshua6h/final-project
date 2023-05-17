"""GUI for baseball stats helper"""

import os
import tkinter as tk
from tkinter import ttk # themed widgets
from tkinter import scrolledtext
from tkinter import *
import use_database
import alchemy
import controller


player_data = []

class App(tk.Frame):
    def __init__(self, parent, player_data):

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.frame.grid(row=0, column=0)
        self.top_frame = ttk.Frame(self)

        league_label = tk.Label(self.frame, text="League Name (name of league file without extension): ")#.pack()
        league_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.league_entry = ttk.Entry(self.frame)#.pack()
        self.league_entry.grid(row=0, column=2, columnspan=1, padx=10, pady=10 )

        order_by_label = tk.Label(self.frame, text="order by: ")#.pack()
        order_by_label.grid(row=1, column=1, pady=10)

        order_by_options = ["ab", "ab", "singles", "doubles", "triples", "home runs", "walks", "raa", "woba"]
        self.order_by_clicked = StringVar()
        self.order_by_clicked.set("woba")
        self.order_by_entry = ttk.OptionMenu(self.frame, self.order_by_clicked, *order_by_options)#.pack()
        self.order_by_entry.grid(row=1, column=2, columnspan=1, padx=10, pady=10 )

        ascdesc_options = ["desc", "asc", "desc"]
        self.ascdesc_clicked = StringVar()
        self.ascdesc_clicked.set("desc")
        self.ascdesc_entry = ttk.OptionMenu(self.frame, self.ascdesc_clicked, *ascdesc_options)#.pack()
        self.ascdesc_entry.grid(row=1, column=3, columnspan=1, padx=10, pady=10 )

        name_label = tk.Label(self.frame, text="name (like): ")#.pack()
        name_label.grid(row=2, column=1, pady=10)

        self.name_entry = ttk.Entry(self.frame)#.pack()
        self.name_entry.grid(row=2, column=2, columnspan=1, padx=10, pady=10 )

        ab_min_label = tk.Label(self.frame, text="Min At Bats: ")#.pack()
        ab_min_label.grid(row=3, column=1, pady=10)

        self.ab_min_entry = ttk.Entry(self.frame)#.pack()
        self.ab_min_entry.grid(row=3, column=2, columnspan=1, padx=10, pady=10 )

        ab_max_label = tk.Label(self.frame, text="Max At Bats: ")#.pack()
        ab_max_label.grid(row=3, column=4, pady=10)

        self.ab_max_entry = ttk.Entry(self.frame)#.pack()
        self.ab_max_entry.grid(row=3, column=5, columnspan=2, padx=10, pady=10 )

        # self.error_msg = StringVar()
        # self.error_msg = ""
        # error_msg = ttk.Label(self.frame, text=self.error_msg)
        # error_msg.grid(row=4, column=0)


        addLeagueButton = tk.Button(self, text = "Add/Overwrite League", command=self.handleAddLeague)
        loadLeagueButton = tk.Button(self, text = "Load League", command=self.handleLoadLeague)
        nextPageButton = tk.Button(self, text = "Next Page", command=self.handleNextPage)
        previousPageButton = tk.Button(self, text = "Previous Page", command=self.handlePreviousPage)

        addLeagueButton.pack()
        loadLeagueButton.pack()
        nextPageButton.pack()
        previousPageButton.pack()

        self.min = 0
        self.max = 15
        self.total_players = 0
        self.player_data = player_data

        self.populate(player_data)
        

    def populate(self, player_data):
        self.total_players = len(player_data)
        self.label_frame = tk.Frame(self.canvas, background="#ffffff")
        self.canvas.create_window((4,4), window=self.label_frame, anchor="nw",
                                  tags="self.label_frame")
        self.label_frame.bind("<Configure>", self.onFrameConfigure)

        self.label_frame.grid(row=1, column=0)

        tk.Label(self.label_frame, text="rank", bg="white", font="bold").grid(row=0, column=0)
        tk.Label(self.label_frame, text="name", bg="white", font="bold").grid(row=0, column=1)
        tk.Label(self.label_frame, text="wOBA", bg="white", font="bold").grid(row=0, column=2)
        tk.Label(self.label_frame, text="RAA", bg="white", font="bold").grid(row=0, column=3)
        tk.Label(self.label_frame, text="at bats", bg="white", font="bold").grid(row=0, column=4)
        tk.Label(self.label_frame, text="singles", bg="white", font="bold").grid(row=0, column=5)
        tk.Label(self.label_frame, text="doubles", bg="white", font="bold").grid(row=0, column=6)
        tk.Label(self.label_frame, text="triples", bg="white", font="bold").grid(row=0, column=7)
        tk.Label(self.label_frame, text="home runs", bg="white", font="bold").grid(row=0, column=8)
        tk.Label(self.label_frame, text="walks", bg="white", font="bold").grid(row=0, column=9)

        i = self.min
        j = 0
        while i < min(self.max, len(player_data)):
            player = player_data[i]
            tk.Label(self.label_frame, text=i + 1, bg="white").grid(row=i + 1, column=0)
            tk.Label(self.label_frame, text=player.name, bg="white").grid(row=i + 1, column=1)
            tk.Label(self.label_frame, text=round(player.wOBA, 3), bg="white").grid(row=i + 1, column=2)
            tk.Label(self.label_frame, text=round(player.RAA, 3), bg="white").grid(row=i + 1, column=3)
            tk.Label(self.label_frame, text=round(player.at_bats, 3), bg="white").grid(row=i + 1, column=4)
            tk.Label(self.label_frame, text=round(player.singles, 3), bg="white").grid(row=i + 1, column=5)
            tk.Label(self.label_frame, text=round(player.doubles, 3), bg="white").grid(row=i + 1, column=6)
            tk.Label(self.label_frame, text=round(player.triples, 3), bg="white").grid(row=i + 1, column=7)
            tk.Label(self.label_frame, text=round(player.home_runs, 3), bg="white").grid(row=i + 1, column=8)
            tk.Label(self.label_frame, text=round(player.walks, 3), bg="white").grid(row=i + 1, column=9)
            i += 1
            j += 1
        

    def clear(self):
        self.label_frame.destroy()

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def handleAddLeague(self):
        league_name = self.league_entry.get()
        success = controller.overwrite_league(league_name)
        if success:
            self.error_msg = ttk.Label(self.frame, text="")
            self.error_msg.grid(row=4, column=0)
            self.error_msg.destroy()
        else:
            self.error_msg = ttk.Label(self.frame, text="Error parsing file " + league_name + ".csv")
            self.error_msg.grid(row=4, column=0)
            
        order_by = self.order_by_clicked.get()
        ascdesc = self.ascdesc_clicked.get()
        name = self.name_entry.get()
        ab_min = self.ab_min_entry.get()
        if ab_min == "":
            ab_min = 0
        elif type(ab_min) != int:
            ab_min = 0

        ab_max = self.ab_max_entry.get()
        if ab_max == "":
            ab_max = 100000
        elif type(ab_max) != int:
            ab_max = 100000

        if not ascdesc:
            ascdesc = 'desc'
        if order_by:
            player_data = alchemy.get_filtered_sorted_players(league_name, order_by, ascdesc, name, ab_min, ab_max)
        else:
            player_data = alchemy.get_filtered_sorted_players(league_name)

        if order_by:
            player_data = alchemy.get_filtered_sorted_players(league_name, order_by, ascdesc)
        else:
            player_data = alchemy.get_filtered_sorted_players(league_name)
        self.clear()
        self.min = 0
        self.max = 15
        self.player_data = player_data
        self.populate(player_data)

    def handleLoadLeague(self):
        league_name = self.league_entry.get()
        order_by = self.order_by_clicked.get()
        ascdesc = self.ascdesc_clicked.get()
        name = self.name_entry.get()
        ab_min = self.ab_min_entry.get()
        ab_max = self.ab_max_entry.get()

        try:
            ab_min = int(ab_min)
        except:
            ab_min = 0

        try:
            ab_max = int(ab_max)
        except:
            ab_max = 100000

        if not ascdesc:
            ascdesc = 'desc'
        if order_by:
            player_data = alchemy.get_filtered_sorted_players(league_name, order_by, ascdesc, name, ab_min, ab_max)
        else:
            player_data = alchemy.get_filtered_sorted_players(league_name)
        if not player_data:
            self.error_msg = ttk.Label(self.frame, text="No players in league " + league_name + " found")
            self.error_msg.grid(row=4, column=0)
        else:
            self.error_msg = ttk.Label(self.frame, text="")
            self.error_msg.grid(row=4, column=0)
            self.error_msg.destroy()

        self.clear()
        self.min = 0
        self.max = 15
        self.player_data = player_data
        self.populate(player_data)

    def handleNextPage(self):
        self.min += 15
        self.max += 15
        if self.min + 1 > self.total_players:
            self.min -= 15
            self.max -= 15
        self.clear()
        self.populate(self.player_data)

    
    def handlePreviousPage(self):
        self.min -= 15
        self.max -= 15
        if self.min < 0:
            self.min = 0
            self.max = 15
        self.clear()
        self.populate(self.player_data)
            


if __name__ == '__main__':

    player_data = alchemy.get_filtered_sorted_players("rock_222")
    root=tk.Tk()
    example = App(root, player_data)
    example.pack(side="top", fill="both", expand=True)
    root.geometry("1100x600")
    root.mainloop()