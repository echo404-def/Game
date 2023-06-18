#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 16:50:02 2023

@author: echo.
"""

import tkinter as tk
from random import choice, randint
import math


class Data:
    width = 1000
    height = 500
    
    ch_image = ["o(｀ω´ )o","(● ˃̶͈̀ロ˂̶͈́)੭ꠥ⁾⁾"]
    ch_size = 20
    ch_state = {"x":width/2, "y":height/2, "image":ch_image[0], "speed":7, "d_x":0, "d_y":0, "fire":False}
    
    shell_image = ["🍅","🥕","🥔","🧅","🥬","🍆","🍖","🧄","🍙","🍌"]
    shell_speed = 9
    shell_cooltime = 0
    shell_cooltime_set = 10
    shell_size = 20
    shell = list()
    
    effect_image = ["💥","🔥","✨"]
    effect_time = 10
    effect_size = 40
    effect = list()
    
    # BG Flash
    flash_color = "maroon"
    flash_time_set = 5
    flash_time = 0
    
    bomb_image = ["💣"]
    money_image = ["💶","💰","💍","💎","💳"]
    enemy_image = ["👾","🦑","🐙","👻"]
    
    entity_speed = -4
    entity_cooltime = 0
    entity_cooltime_set = 40
    entity_size = 50
    entity = list()
    
    score = 0
    
    hp_image = ["❤️","♡"]
    hp_full = 3
    hp = hp_full
    
    # Switching screens
    screen = "start"




class Start:
    def pressed_st(self,event):
        self.screen = "main"
    
    def start(self):
        self.canvas["bg"] = "black"
        self.canvas.create_text(self.width//2,self.height//2-30,text="Yasai Nageru Man",fill="lightgreen",font=("Arial",80,"bold"))
        self.canvas.create_text(self.width//2,self.height//2+50,text="- Press Return -",fill="white",font=("Arial",20,"bold"))
        self.root.title("Yasai Nageru Man")
        self.root.bind("<Return>",self.pressed_st)


class Gameover:
    def pressed_gmo(self,event):
        self.reset()
        self.screen = "start"
    
    def gameover(self):
        self.canvas["bg"] = "black"
        self.canvas.create_text(self.width//2,self.height//2-60,text="Game Over",fill="red",font=("Arial",80,"bold"))
        self.canvas.create_text(self.width//2,self.height//2+40,text=f"SCORE: {self.score}",fill="white",font=("Arial",20,"bold"))
        self.canvas.create_text(self.width//2,self.height//2+80,text="- Press Return -",fill="gray",font=("Arial",20))
        self.root.title("Game Over")
        self.root.bind("<Return>",self.pressed_gmo)



class StatesBar:
    def update_title(self):
        hp = f"{self.hp_image[0]*self.hp}{self.hp_image[1]*(self.hp_full-self.hp)}"
        score = str(self.score).zfill(3)
        text = f"HP:{hp}      SCORE:{score}"
        self.root.title(text)



class Main(Data,Start,Gameover,StatesBar):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.config(bg="black")
        self.canvas = tk.Canvas(self.root,width=self.width,height=self.height,bg="black")
        self.canvas.pack()
        self.update()
    
    
    # Reset
    def reset(self):
        self.shell = []
        self.entity = []
        self.ch_state = {"x":self.width/2, "y":self.height/2, "image":self.ch_image[0], "speed":7, "d_x":0, "d_y":0, "fire":False}
        self.score = 0
        self.hp = self.hp_full
        
        
    
    
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
        
        
        
        
        
    
    # Collision
    # オブジェクトを呼び出す回数を減らすためにmove_entityに組み込む
    def check_collision(self,x1, y1, r1, x2, y2, r2):
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if distance < r1 + r2:
            return True
        else:
            return False
        
        
        
    # Effect
    def add_effect(self,x,y,types):
        if types == "damage":
            image = self.effect_image[randint(0,1)]
        elif types == "money":
            image = self.effect_image[2]
        effect = {"x":x,"y":y,"image":image,"time":self.effect_time}
        self.effect.append(effect)
            
        
    def update_effect(self):
        for effect in self.effect:
            if effect["time"] <= 0:
                self.effect.remove(effect)
            else:
                effect["time"] -= 1
                self.canvas.create_text(effect["x"],effect["y"],text=effect["image"],font=("Arial",self.effect_size),fill="red")
        
        
        
    # BG Flash
    def flash(self):
        if self.flash_time > 0:
            self.canvas["bg"] = self.flash_color
            self.flash_time -= 1
        else:
            if self.canvas["bg"] != "black":
                self.canvas["bg"] = "black"
        
        
        
    # Enttity (enemy & money)
    def summon_entity(self):
        if self.entity_cooltime == 0:
            if randint(0,4):
                n = randint(1,10)
                if n == 1:
                    state = {"x":self.width,"y":randint(30,self.height-30),"image":choice(self.money_image),"type":"money"}
                elif n == 2:
                    state = {"x":self.width,"y":randint(30,self.height-30),"image":choice(self.bomb_image),"type":"bomb"}
                else:
                    y = randint(50,self.height-50)
                    state = {"x":self.width,"y":y,"image":choice(self.enemy_image),"type":"enemy","home_y":y,"d_y":randint(1,5)}
                self.entity.append(state)
            self.entity_cooltime = self.entity_cooltime_set
    
    def move_entity(self):
        for state in self.entity:
            if state["x"] <= 0:
                self.entity.remove(state)
                if state["type"] == "enemy":
                    self.hp -= 1
                    self.flash_time = self.flash_time_set
            else:
                state["x"] += self.entity_speed
                if state["type"] == "enemy":
                    state["x"] += 1 # speed down
                    state["y"] += state["d_y"]
                    if state["y"] > state["home_y"]+50 or state["y"] < state["home_y"]-50:
                        state["d_y"] *= -1
            # Collision
                # Entity hit Charactor
                if self.check_collision(state["x"], state["y"], 25, self.ch_state["x"], self.ch_state["y"], self.ch_size//2):
                    if state["type"] == "enemy":
                        self.entity.remove(state)
                        self.hp -= 1
                        self.add_effect(state["x"], state["y"], "damage")
                        self.flash_time = self.flash_time_set
                    elif state["type"] == "money":
                        n = 5 * (self.money_image.index(state["image"]) + 1)
                        self.score += n
                        self.entity.remove(state)
                        self.add_effect(state["x"], state["y"], "money")
                    elif state["type"] == "bomb":
                        self.hp -= 1
                        self.add_effect(state["x"], state["y"], "damage")
                        self.entity.remove(state)
                        self.flash_time = self.flash_time_set
                # Entity hit Shell
                for shell in self.shell:
                    if self.check_collision(state["x"], state["y"], 25, shell["x"], shell["y"], 10):
                        self.add_effect(state["x"], state["y"], "damage")
                        self.entity.remove(state)
                        self.shell.remove(shell)
                        print("\a",end=("")) # Sound
                        if state["type"] == "bomb":
                            self.flash_time = self.flash_time_set
                            self.hp -= 1
                        else:
                            self.score += 1
                # Draw on new position
                self.canvas.create_text(state["x"],state["y"],text=state["image"],font=("",self.entity_size),fill="green")
        if self.entity_cooltime > 0:
            self.entity_cooltime -= 1
    
        
        
        
    # Key input
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
    def main(self):
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
        self.canvas.create_text(self.ch_state["x"],self.ch_state["y"], text=self.ch_state["image"],font=("",self.ch_size,"bold"),fill="white")
        
        # Title
        self.update_title()
        
        # BG Flash
        self.flash()
        
        # Draw Effect
        self.update_effect()
        
        # GameOver
        if self.hp <= 0:
            self.screen = "gameover"
    
    def update(self):
        # Reset Display
        self.canvas.delete("all")
        if self.screen == "main":
            self.main()
        elif self.screen == "gameover":
            self.gameover()
        elif self.screen == "start":
            self.start()
        
    
        self.canvas.after(12,self.update)
        

        
if __name__ == "__main__":
    f = Main()
    f.root.mainloop()
    