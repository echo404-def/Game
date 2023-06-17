#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 16:50:02 2023

@author: echo.
"""

import tkinter as tk
from random import choice, randint

class Data:
    width = 1000
    height = 500
    
    ch_image = ["o(｀ω´ )o","(● ˃̶͈̀ロ˂̶͈́)੭ꠥ⁾⁾"]
    ch_state = {"x":width/2, "y":height/2, "image":ch_image[0], "speed":7, "d_x":0, "d_y":0, "fire":False}
    
    shell_image = ["🍅","🥕","🥔","🧅","🥬","🍆","🍖","🧄","🍙","🍌"]
    shell_speed = 9
    shell_cooltime = 0
    shell_cooltime_set = 10
    shell_size = 20
    shell = list()
    
    damage_image = ["💥","🔥"]
    
    money_image = ["💶","💰","💍","💎","💳"]
    enemy_image = ["👾","🦑","🐙","👻"]
    
    entity_speed = -4
    entity_cooltime = 0
    entity_cooltime_set = 50
    entity_size = 50
    entity = list()




class Main(Data):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.config(bg="black")
        self.canvas = tk.Canvas(self.root,width=self.width,height=self.height,bg="black")
        self.canvas.pack()
        self.update()
    
    
    
    
    # Shell
    def fire_shell(self):
        if self.shell_cooltime == 0:
            state = {"x":self.ch_state["x"],"y":self.ch_state["y"],"image":choice(self.shell_image)}
            self.shell.append(state)
            self.shell_cooltime = self.shell_cooltime_set
        
    def move_shell(self):
        for state in self.shell:
            # Delete shell going off screen.
            if state["x"] > self.width:
                self.shell.remove(state)
            else:
                state["x"] += self.shell_speed
                self.canvas.create_text(state["x"],state["y"],text=state["image"],font=("",self.shell_size),fill="orange")
        # Countdown cooltime
        if self.shell_cooltime > 0:
            self.shell_cooltime -= 1
        
        
        
        
    # Enemy & Money (Entity)
    def summon_entity(self):
        if self.entity_cooltime == 0:
            if randint(0,4):
                if randint(1,10) == 1:
                    state = {"x":self.width,"y":randint(30,self.height-30),"image":choice(self.money_image),"type":"money"}
                else:
                    y = randint(50,self.height-50)
                    state = {"x":self.width,"y":y,"image":choice(self.enemy_image),"type":"enemy","home_y":y,"d_y":randint(1,5)}
                self.entity.append(state)
            self.entity_cooltime = self.entity_cooltime_set
    
    def move_entity(self):
        for state in self.entity:
            if state["x"] <= 0:
                self.entity.remove(state)
            else:
                state["x"] += self.entity_speed
                if state["type"] == "enemy":
                    state["x"] += 1 # boost
                    state["y"] += state["d_y"]
                    if state["y"] > state["home_y"]+50 or state["y"] < state["home_y"]-50:
                        state["d_y"] *= -1
                self.canvas.create_text(state["x"],state["y"],text=state["image"],font=("",self.entity_size),fill="green")
        if self.entity_cooltime > 0:
            self.entity_cooltime -= 1
    
        
        
        
    # Key
    def pressed(self,event):
        key = event.keysym
        if key == "d":
            self.ch_state["d_x"] = self.ch_state["speed"]
        elif key == "a":
            self.ch_state["d_x"] = self.ch_state["speed"] * -1
        if key == "s":
            self.ch_state["d_y"] = self.ch_state["speed"]
        elif key == "w":
            self.ch_state["d_y"] = self.ch_state["speed"] * -1
        if key == "space":
            self.ch_state["fire"] = True
            self.ch_state["image"] = self.ch_image[1]
    
    def release(self,event):
        key = event.keysym
        if key == "d" or key == "a":
            self.ch_state["d_x"] = 0
        if key == "s" or key == "w":
            self.ch_state["d_y"] = 0
        if key == "space":
            self.ch_state["fire"] = False
            self.ch_state["image"] = self.ch_image[0]
            
            
            
            
    # Prevents going off screen.
    def wall(self):
        if self.ch_state["x"] <= 50:
            if self.ch_state["d_x"] < 0:
                self.ch_state["d_x"] = 0
        elif self.ch_state["x"] >= self.width - 50:
            if self.ch_state["d_x"] > 0:
                self.ch_state["d_x"] = 0
        if self.ch_state["y"] <= 25:
            if self.ch_state["d_y"] < 0:
                self.ch_state["d_y"] = 0
        elif self.ch_state["y"] >= self.height - 25:
            if self.ch_state["d_y"] > 0:
                self.ch_state["d_y"] = 0
        
        
        
    # Main Loop
    def update(self):
        # Reset Display
        self.canvas.delete("all")
        
        # Get Key input
        self.root.bind("<KeyPress>",self.pressed)
        self.root.bind("<KeyRelease>",self.release)
        
        # Prevents going off screen.
        self.wall()
        
        # Draw Shell
        if self.ch_state["fire"]:
            self.fire_shell()
        self.move_shell()
        
        # Draw Entity
        self.summon_entity()
        self.move_entity()
        
        # Draw Main characotr
        self.ch_state["x"] += self.ch_state["d_x"]
        self.ch_state["y"] += self.ch_state["d_y"]
        self.canvas.create_text(self.ch_state["x"],self.ch_state["y"], text=self.ch_state["image"],font=("",20),fill="white")
        self.canvas.after(12,self.update)
        
if __name__ == "__main__":
    f = Main()
    f.root.mainloop()
    