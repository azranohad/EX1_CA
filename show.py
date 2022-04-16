from tkinter import Canvas, Tk
master = Tk()

w = Canvas(master, width=1000, height=1000, bg = "black")

w.create_rectangle(995, 995, 1000, 1000, fill="blue", outline='blue')
w.create_rectangle(0, 0, 5, 5, fill="red", outline='blue')
w.create_rectangle(0, 995, 5, 1000, fill="red", outline='blue')
w.create_rectangle(995, 0, 1000, 5, fill="red", outline='blue')
w.pack()
master.mainloop()


# import Tkinter as tk
# import random
#
# class App(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#         self.canvas = tk.Canvas(self, width=500, height=500, borderwidth=0, highlightthickness=0)
#         self.canvas.pack(side="top", fill="both", expand="true")
#         self.rows = 100
#         self.columns = 100
#         self.cellwidth = 25
#         self.cellheight = 25
#
#         self.rect = {}
#         self.oval = {}
#         for column in range(20):
#             for row in range(20):
#                 x1 = column*self.cellwidth
#                 y1 = row * self.cellheight
#                 x2 = x1 + self.cellwidth
#                 y2 = y1 + self.cellheight
#                 self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="blue", tags="rect")
#                 self.oval[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="blue", tags="oval")
#
#         self.redraw(1000)
#
#     def redraw(self, delay):
#         self.canvas.itemconfig("rect", fill="blue")
#         self.canvas.itemconfig("oval", fill="blue")
#         for i in range(10):
#             row = random.randint(0,19)
#             col = random.randint(0,19)
#             item_id = self.oval[row,col]
#             self.canvas.itemconfig(item_id, fill="green")
#         self.after(delay, lambda: self.redraw(delay))
#
# if __name__ == "__main__":
#     app = App()
#     app.mainloop()

# from tkinter import *  # not a good idea in my opinion, can lead to accidental
#                        # naming conflicts, "import tkinter as tk" is a better alternative
# import numpy as np
# import matplotlib.pyplot as plt
# #~from board import Board
# from PIL import Image, ImageTk
# from matplotlib.backends.backend_tkagg import (
#     FigureCanvasTkAgg, NavigationToolbar2Tk)
#
# def num():
#     n1 = int(t1.get())
#     n2 = int(t2.get())
#     n3 = int(t3.get()) / 100.00
#     top.destroy()  # close dialog
#     initBoard = np.zeros((200, 200))
#     for row in range(0, n1):
#         for column in range(0, n2):
#             initBoard[row][column] = np.random.choice(np.arange(0, 2), p=[1 - n3, n3])
#     #game_board = Board(n1, n2, initBoard)
#     ax.imshow(initBoard)  # draw board
#     canvas.draw_idle()  # update matplotlib figure
#
# root = Tk()
# root.title('Game of Life')
# root.geometry('800x600')
# # create matplotlib figure
# fig = plt.figure()
# ax = fig.add_subplot(111)  # create axis
# ax.axis('off')
# canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
# canvas.get_tk_widget().grid(row=4, column=0)
#
# # toplevel to choose parameters
# top = Toplevel(root)
# Label(top, text="How many rows?: ").grid(row=0)
# Label(top, text="How many columns?: ").grid(row=1)
# Label(top, text="Probability of spawn (between 0 and 100): ").grid(row=2)
#
# t1 = Entry(top)
# t2 = Entry(top)
# t3 = Entry(top)
#
# t1.grid(row=0, column=1)
# t2.grid(row=1, column=1)
# t3.grid(row=2, column=1)
#
# Button(top, text='Generate', command=num).grid(row=3, column=1, sticky=W, pady=4)
#
# mainloop()


# importing all necessary libraries
# import random
# import tkinter
# from tkinter import *
# from functools import partial
# from tkinter import messagebox
# from copy import deepcopy
#
# # sign variable to decide the turn of which player
# sign = 0
#
# # Creates an empty board
# global board
# board = [[" " for x in range(200)] for y in range(200)]
#
#
# # Check l(O/X) won the match or not
# # according to the rules of the game
# def winner(b, l):
#     return ((b[0][0] == l and b[0][1] == l and b[0][2] == l) or
#             (b[1][0] == l and b[1][1] == l and b[1][2] == l) or
#             (b[2][0] == l and b[2][1] == l and b[2][2] == l) or
#             (b[0][0] == l and b[1][0] == l and b[2][0] == l) or
#             (b[0][1] == l and b[1][1] == l and b[2][1] == l) or
#             (b[0][2] == l and b[1][2] == l and b[2][2] == l) or
#             (b[0][0] == l and b[1][1] == l and b[2][2] == l) or
#             (b[0][2] == l and b[1][1] == l and b[2][0] == l))
#
#
# # Configure text on button while playing with another player
# def get_text(i, j, gb, l1, l2):
#     global sign
#     if board[i][j] == ' ':
#         if sign % 2 == 0:
#             l1.config(state=DISABLED)
#             l2.config(state=ACTIVE)
#             board[i][j] = "X"
#         else:
#             l2.config(state=DISABLED)
#             l1.config(state=ACTIVE)
#             board[i][j] = "O"
#         sign += 1
#         button[i][j].config(text=board[i][j])
#     if winner(board, "X"):
#         gb.destroy()
#         box = messagebox.showinfo("Winner", "Player 1 won the match")
#     elif winner(board, "O"):
#         gb.destroy()
#         box = messagebox.showinfo("Winner", "Player 2 won the match")
#     elif (isfull()):
#         gb.destroy()
#         box = messagebox.showinfo("Tie Game", "Tie Game")
#
#
# # Check if the player can push the button or not
# def isfree(i, j):
#     return board[i][j] == " "
#
#
# # Check the board is full or not
# def isfull():
#     flag = True
#     for i in board:
#         if (i.count(' ') > 0):
#             flag = False
#     return flag
#
#
# # Create the GUI of game board for play along with another player
# def gameboard_pl(game_board, l1, l2):
#     global button
#     button = []
#     for i in range(200):
#         m = 200 + i
#         button.append(i)
#         button[i] = []
#         for j in range(200):
#             n = j
#             button[i].append(j)
#             get_t = partial(get_text, i, j, game_board, l1, l2)
#             button[i][j] = Button(
#                 game_board, bd=5, command=get_t, height=4, width=8)
#             button[i][j].grid(row=m, column=n)
#     game_board.mainloop()
#
#
# # Decide the next move of system
# def pc():
#     possiblemove = []
#     for i in range(len(board)):
#         for j in range(len(board[i])):
#             if board[i][j] == ' ':
#                 possiblemove.append([i, j])
#     move = []
#     if possiblemove == []:
#         return
#     else:
#         for let in ['O', 'X']:
#             for i in possiblemove:
#                 boardcopy = deepcopy(board)
#                 boardcopy[i[0]][i[1]] = let
#                 if winner(boardcopy, let):
#                     return i
#         corner = []
#         for i in possiblemove:
#             if i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
#                 corner.append(i)
#         if len(corner) > 0:
#             move = random.randint(0, len(corner) - 1)
#             return corner[move]
#         edge = []
#         for i in possiblemove:
#             if i in [[0, 1], [1, 0], [1, 2], [2, 1]]:
#                 edge.append(i)
#         if len(edge) > 0:
#             move = random.randint(0, len(edge) - 1)
#             return edge[move]
#
#
# # Configure text on button while playing with system
# def get_text_pc(i, j, gb, l1, l2):
#     global sign
#     if board[i][j] == ' ':
#         if sign % 2 == 0:
#             l1.config(state=DISABLED)
#             l2.config(state=ACTIVE)
#             board[i][j] = "X"
#         else:
#             button[i][j].config(state=ACTIVE)
#             l2.config(state=DISABLED)
#             l1.config(state=ACTIVE)
#             board[i][j] = "O"
#         sign += 1
#         button[i][j].config(text=board[i][j])
#     x = True
#     if winner(board, "X"):
#         gb.destroy()
#         x = False
#         box = messagebox.showinfo("Winner", "Player won the match")
#     elif winner(board, "O"):
#         gb.destroy()
#         x = False
#         box = messagebox.showinfo("Winner", "Computer won the match")
#     elif (isfull()):
#         gb.destroy()
#         x = False
#         box = messagebox.showinfo("Tie Game", "Tie Game")
#     if (x):
#         if sign % 2 != 0:
#             move = pc()
#             button[move[0]][move[1]].config(state=DISABLED)
#             get_text_pc(move[0], move[1], gb, l1, l2)
#
#
# # Create the GUI of game board for play along with system
# def gameboard_pc(game_board, l1, l2):
#     global button
#     button = []
#     for i in range(200):
#         m = 200 + i
#         button.append(i)
#         button[i] = []
#         for j in range(200):
#             n = j
#             button[i].append(j)
#             get_t = partial(get_text_pc, i, j, game_board, l1, l2)
#             button[i][j] = Button(
#                 game_board, bd=5, command=get_t, height=1, width=1)
#             button[i][j].grid(row=m, column=n)
#     game_board.mainloop()
#
#
# # Initialize the game board to play with system
# def withpc(game_board):
#     game_board.destroy()
#     game_board = Tk()
#     game_board.title("Tic Tac Toe")
#     l1 = Button(game_board, text="Player : X", width=10)
#     l1.grid(row=1, column=1)
#     l2 = Button(game_board, text="Computer : O",
#                 width=10, state=DISABLED)
#
#     l2.grid(row=2, column=1)
#     gameboard_pc(game_board, l1, l2)
#
#
# # Initialize the game board to play with another player
# def withplayer(game_board):
#     game_board.destroy()
#     game_board = Tk()
#     game_board.title("Tic Tac Toe")
#     l1 = Button(game_board, text="Player 1 : X", width=10)
#
#     l1.grid(row=1, column=1)
#     l2 = Button(game_board, text="Player 2 : O",
#                 width=10, state=DISABLED)
#
#     l2.grid(row=2, column=1)
#     gameboard_pl(game_board, l1, l2)
#
#
# # main function
# def play():
#     menu = Tk()
#     menu.geometry("250x250")
#     menu.title("Tic Tac Toe")
#     wpc = partial(withpc, menu)
#     wpl = partial(withplayer, menu)
#
#     head = Button(menu, text="---Welcome to tic-tac-toe---",
#                   activeforeground='red',
#                   activebackground="yellow", bg="red",
#                   fg="yellow", width=500, font='summer', bd=5)
#
#     B1 = Button(menu, text="Single Player", command=wpc,
#                 activeforeground='red',
#                 activebackground="yellow", bg="red",
#                 fg="yellow", width=500, font='summer', bd=5)
#
#     B2 = Button(menu, text="Multi Player", command=wpl, activeforeground='red',
#                 activebackground="yellow", bg="red", fg="yellow",
#                 width=500, font='summer', bd=5)
#
#     B3 = Button(menu, text="Exit", command=menu.quit, activeforeground='red',
#                 activebackground="yellow", bg="red", fg="yellow",
#                 width=500, font='summer', bd=5)
#     head.pack(side='top')
#     B1.pack(side='top')
#     B2.pack(side='top')
#     B3.pack(side='top')
#     menu.mainloop()
#
#
# # Call main function
# if __name__ == '__main__':
#     play()