#importing libraries
import tkinter as tk
from functools import partial
import random
import time

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

#game text
game_txt = tk.Label(
)
#padding above, below
game_txt.pack(pady=(20, 5))

txt_done = [None] #list so changeable in function
#ending typing 
def tpg_end(root, txt_done):
  if txt_done[0] is not None:
     root.after_cancel(txt_done[0])
     txt_done[0] = None

#skip typing effect
def tpg_skip(event=None, txt=None):
    if txt_done[0] is not None and txt is not None:
        update_gui(txt, index=0, txt_done=txt_done, skip=True)

#update gui, end/remove text when start
def update_gui(txt, index=0, txt_done=txt_done, skip=False):
  if index == 0:
      game_txt.bind("<Button-1>", partial(tpg_skip, txt=txt))
      tpg_end(root, txt_done=txt_done)
      game_txt.config(text="")

  #skips typing effect
  if skip:
     game_txt.config(text=txt)
     tpg_end(root, txt_done)
     return
  #wait after printing character for typing effect
  if index < len(txt):
        game_txt.config(text=game_txt.cget("text") + txt[index])
        txt_done[0] = root.after(50, update_gui, txt, index + 1)

update_gui(txt=("testing, testing\ntesting"))
root.mainloop()

