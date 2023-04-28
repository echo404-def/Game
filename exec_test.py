#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 11:32:10 2023

@author: ahitochigaidesu.
"""

import tkinter as tk


class Data:
    pass


def press():
    inp = text.get(1.0,tk.END)
    try:
        print(eval(inp))
    except:
        try:
            exec(inp)
        except:
            print("ERROR\a")


root = tk.Tk()

text = tk.Text(bg="black",fg="lightgreen")
text.config(insertbackground="orange")
text.pack()

btn1 = tk.Button(root,text="run",command=press)
btn1.pack()

root.mainloop()
