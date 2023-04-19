"""GUI for baseball stats helper"""

import os
import tkinter as tk
from tkinter import ttk # themed widgets
from tkinter import scrolledtext
from tkinter import *
import use_database


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

        self.populate(player_data)

    def populate(self, player_data):
        tk.Label(self.frame, text="name", bg="white", font="bold").grid(row=0, column=0)
        tk.Label(self.frame, text="wOBA", bg="white", font="bold").grid(row=0, column=1)
        tk.Label(self.frame, text="RAA", bg="white", font="bold").grid(row=0, column=2)
        tk.Label(self.frame, text="at bats", bg="white", font="bold").grid(row=0, column=3)
        tk.Label(self.frame, text="singles", bg="white", font="bold").grid(row=0, column=4)
        tk.Label(self.frame, text="doubles", bg="white", font="bold").grid(row=0, column=5)
        tk.Label(self.frame, text="triples", bg="white", font="bold").grid(row=0, column=6)
        tk.Label(self.frame, text="home runs", bg="white", font="bold").grid(row=0, column=7)
        tk.Label(self.frame, text="walks", bg="white", font="bold").grid(row=0, column=8)

        for i in range(len(player_data)):
            player = player_data[i]
            tk.Label(self.frame, text=player.name, bg="white").grid(row=i + 1, column=0)
            tk.Label(self.frame, text=round(player.wOBA, 3), bg="white").grid(row=i + 1, column=1)
            tk.Label(self.frame, text=round(player.RAA, 3), bg="white").grid(row=i + 1, column=2)
            tk.Label(self.frame, text=round(player.at_bats, 3), bg="white").grid(row=i + 1, column=3)
            tk.Label(self.frame, text=round(player.singles, 3), bg="white").grid(row=i + 1, column=4)
            tk.Label(self.frame, text=round(player.doubles, 3), bg="white").grid(row=i + 1, column=5)
            tk.Label(self.frame, text=round(player.triples, 3), bg="white").grid(row=i + 1, column=6)
            tk.Label(self.frame, text=round(player.home_runs, 3), bg="white").grid(row=i + 1, column=7)
            tk.Label(self.frame, text=round(player.walks, 3), bg="white").grid(row=i + 1, column=8)


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



if __name__ == '__main__':

    player_data = use_database.get_all_players("rock_2022")
    root=tk.Tk()
    example = App(root, player_data)
    example.pack(side="top", fill="both", expand=True)
    root.geometry("800x600")
    root.mainloop()