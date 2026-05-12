#importing libraries
import tkinter as tk
from functools import partial
import random

#main colors for gui
bglbl_clr = "#AD9BC2" #main text highlight color
txtbg_bar_clr = "#CCC9FE" #input bar bg
txt_bar_clr = "#E6C9FE" #user input text color
txt_clr = "#FEC9E1" #main text color & button bg color
btn_press_bg = "#B799C9"
btn_txt_clr = "#9A68BA"
font = "OpenDyslexic"
fontsize = 12

#creating gui window
root = tk.Tk()
root.geometry("700x620")
root.title("Lv3game")
root.configure(bg=bglbl_clr) #background color

input_button = tk.Button(
    root,
    text="Input btn",
    bg=txt_clr, #bg color
    fg=btn_txt_clr, #text color
    activebackground=btn_press_bg, #will change to this color when pressed
    font=(font, fontsize, "bold"))

#button space 10 above, 20 below
input_button.pack(pady=(50, 20))


root.mainloop()

