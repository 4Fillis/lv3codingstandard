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
    #uses lambda function to send ca and paths_dict to function
    #command=lambda: user_input(paths_dict, event=None),
    bg=txt_clr, #bg color
    fg=btn_txt_clr, #text color
    activebackground=btn_press_bg, #will change to this color when pressed
    font=(font, fontsize, "bold"))

#entry box frame, padx & pady are text input space
entry_frame = tk.Frame(root, bg=txt_clr, padx=0, pady=0)
entry_frame.pack()

#input bar + button
input_bar = tk.Entry(
    entry_frame,
    width=30,
    relief="solid", #border style
    borderwidth=2,
    bg=txtbg_bar_clr, #input box bg color
    fg=txt_bar_clr, #text color
    font=(font, fontsize, 'bold')
)
input_bar.pack()
#uses lambda to use function with specs in brackets
#input_bar.bind("<Return>", lambda event: user_input(paths_dict, event))


#button space 10 above, 20 below
input_button.pack(pady=(50, 20))


root.mainloop()

