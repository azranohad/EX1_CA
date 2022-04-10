from tkinter import *  # not a good idea in my opinion, can lead to accidental
                       # naming conflicts, "import tkinter as tk" is a better alternative
import numpy as np
import matplotlib.pyplot as plt
#~from board import Board
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

def num():
    n1 = int(t1.get())
    n2 = int(t2.get())
    n3 = int(t3.get()) / 100.00
    top.destroy()  # close dialog
    initBoard = np.zeros((200, 200))
    for row in range(0, n1):
        for column in range(0, n2):
            initBoard[row][column] = np.random.choice(np.arange(0, 2), p=[1 - n3, n3])
    #game_board = Board(n1, n2, initBoard)
    ax.imshow(initBoard)  # draw board
    canvas.draw_idle()  # update matplotlib figure

root = Tk()
root.title('Game of Life')
root.geometry('800x600')
# create matplotlib figure
fig = plt.figure()
ax = fig.add_subplot(111)  # create axis
ax.axis('off')
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.get_tk_widget().grid(row=4, column=0)

# toplevel to choose parameters
top = Toplevel(root)
Label(top, text="How many rows?: ").grid(row=0)
Label(top, text="How many columns?: ").grid(row=1)
Label(top, text="Probability of spawn (between 0 and 100): ").grid(row=2)

t1 = Entry(top)
t2 = Entry(top)
t3 = Entry(top)

t1.grid(row=0, column=1)
t2.grid(row=1, column=1)
t3.grid(row=2, column=1)

Button(top, text='Generate', command=num).grid(row=3, column=1, sticky=W, pady=4)

mainloop()