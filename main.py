from random import randrange, choice, choices

from tkinter import Canvas, Tk, NW, ttk
from tkinter import *

import numpy as np
from PIL import Image, ImageTk
from matplotlib import pyplot as plt, cm, colors
from matplotlib.colors import ListedColormap

master = Tk()
from creature import creature
import random
import time

regularCreaturesSet = set()
infectedSet = set()
recoverSet = set()
list_of_counts = []

c_map_rec_empty = colors.ListedColormap(['#ffffff', '#0515f2', '#f20505'])
c_map_stn = colors.ListedColormap(['#ffffff', '#0515f2', '#f20505', '#e4f002'])


hsv_modified = cm.get_cmap('hsv', 256)# create new hsv colormaps in range of 0.3 (green) to 0.7 (blue)
newcmp = ListedColormap(hsv_modified(np.linspace(0, 1, 256)))# show figure

def initCreatures(numOfCreature, percentageOfSick, percentageOfHyper):
    sim_map = {}
    size = 200
    numOfSick = int(numOfCreature*percentageOfSick)
    numOfHyper = int(numOfCreature*percentageOfHyper)
    i = 0
    while i < numOfCreature:
        if i < numOfSick:
            newPoint = (randrange(size), randrange(size))
            if newPoint in sim_map.keys():
               continue
            else:
               sim_map[newPoint] = creature(False, 1)
               infectedSet.add(newPoint)
        else:
            newPoint = (randrange(size), randrange(size))
            if newPoint in sim_map.keys():
               continue
            else:
               sim_map[newPoint] = creature(False)
               regularCreaturesSet.add(newPoint)

        i = i+1

    sim_map_clone = sim_map.copy()
    for j in range(numOfHyper):
        hyperCreature = choice(list(sim_map_clone.keys()))
        sim_map[hyperCreature].hyper = True
        sim_map_clone.pop(hyperCreature)
    return sim_map
#
# def simInfected(oldSimMap, simKeys, probOfInfect):
#     halfNewSimMap = oldSimMap.copy()
#     isSickList = [0, 1]
#     for key in simKeys:
#         if oldSimMap[key].infected > 0:
#             for x_step in range(-1, 2):
#                 for y_step in range(-1, 2):
#                     if x_step == 0 and y_step == 0:
#                         continue
#                     neighbor_to_check = (key[0] + x_step) % 200, (key[1] + y_step) % 200
#                     if neighbor_to_check in oldSimMap.keys():
#                         if choices(isSickList, weights=(1 - probOfInfect, probOfInfect), k=1)[0] == 1 and \
#                                 halfNewSimMap[neighbor_to_check].infected == 0:
#                             halfNewSimMap[neighbor_to_check].infected = 1
#                             if neighbor_to_check not in regularCreaturesSet:
#                                 x = 3
#                             regularCreaturesSet.remove(neighbor_to_check)
#                             infectedSet.add(neighbor_to_check)
#
#
#     return halfNewSimMap
def simInfected(oldSimMap, probOfInfect):
    halfNewSimMap = oldSimMap.copy()
    isSickList = [0, 1]
    infectedSetCopy = infectedSet.copy()
    for key in infectedSetCopy:
        for x_step in range(-1, 2):
            for y_step in range(-1, 2):
                if x_step == 0 and y_step == 0:
                    continue
                neighbor_to_check = (key[0] + x_step) % 200, (key[1] + y_step) % 200
                if neighbor_to_check in regularCreaturesSet:
                    if choices(isSickList, weights=(1 - probOfInfect, probOfInfect), k=1)[0] == 1:
                        if neighbor_to_check not in halfNewSimMap:
                            x = 3
                        halfNewSimMap[neighbor_to_check].infected = 1
                        regularCreaturesSet.remove(neighbor_to_check)
                        print("remove" + str(neighbor_to_check))
                        infectedSet.add(neighbor_to_check)


    return halfNewSimMap

def simNextGeneration(oldSimMap, halfNewSimMap, numOfGenToRecovery):
    newSimMap = halfNewSimMap.copy()
    simKeys = halfNewSimMap.keys()
    for key in simKeys:
        if oldSimMap[key].infected > 0 and oldSimMap[key].infected < numOfGenToRecovery:
            newSimMap[key].infected = newSimMap[key].infected + 1
        elif oldSimMap[key].infected == numOfGenToRecovery:
            newSimMap[key].infected = -1
            infectedSet.remove(key)
            recoverSet.add(key)
    return newSimMap


def get_new_point(creature_point, is_hyper):
    move_step = tuple()
    if not is_hyper:
        move_step = (random.randint(-1, 1), random.randint(-1, 1))
    else:
        move_step = (random.randint(-10, 10), random.randint(-10, 10))
    return (creature_point[0] + move_step[0]) % 200, (creature_point[1] + move_step[1]) % 200

def simMoveStep(halfNewSimMap):
    oldMap = halfNewSimMap.copy()
    newMap = {}
    while len(oldMap.keys()) > 0:
        creature_point = oldMap.popitem()
        new_point = get_new_point(creature_point[0], creature_point[1].hyper)
        while new_point in newMap.keys() or new_point in oldMap.keys():
            new_point = get_new_point(creature_point[0], creature_point[1].hyper)

        newMap[new_point] = creature_point[1]
        if creature_point[0] in regularCreaturesSet:
            regularCreaturesSet.remove(creature_point[0])
            regularCreaturesSet.add(new_point)
        elif creature_point[0] in infectedSet:
            infectedSet.remove(creature_point[0])
            infectedSet.add(new_point)

        elif creature_point[0] in recoverSet:
            recoverSet.remove(creature_point[0])
            recoverSet.add(new_point)
    return newMap

# def simMoveStep(halfNewSimMap):
#     oldMap = halfNewSimMap.copy()
#     simKeys = halfNewSimMap.keys()
#
#     newMap = {}
#     movesList = [-1,0,1]
#     hyperMovesList = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
#
#     while oldMap:
#         chosenCreature = choice(list(oldMap.keys()))
#         if oldMap[chosenCreature].hyper == False:
#             choiceList = choices(movesList, k=2)
#         else:
#             choiceList = choices(hyperMovesList, k=2)
#
#         firstTuple = (chosenCreature[0] + choiceList[0]) % 200
#         secondTuple = (chosenCreature[1] + choiceList[1]) % 200
#         if (firstTuple, secondTuple) not in newMap:
#             newMap[(firstTuple, secondTuple)] = oldMap[chosenCreature]
#             if newMap[(firstTuple, secondTuple)].infected > 0:
#                 infectedSet.add((firstTuple, secondTuple))
#             elif newMap[(firstTuple, secondTuple)].infected <= 0:
#                 regularCreaturesSet.add((firstTuple, secondTuple))
#             oldMap.pop(chosenCreature)
#     return newMap, regularCreaturesSet, infectedSet



def coronaSimulation(numOfCreature,percentageOfSick,percentageOfHyper,numOfGenToRecovery,probOfInfectHigh,probOfInfectLow,treshhold):
    oldSimMap = initCreatures(numOfCreature, percentageOfSick, percentageOfHyper)
    #show simulation
    nrows = 800
    ncols = 800



    win = Tk()
    w = Canvas(master, width=1000, height=800, bg="white")
    plt.title("Matplotlib pcolormesh")

    for i in range(1000):
        print(i)
        list_of_counts.append((i, len(regularCreaturesSet), len(infectedSet), len(recoverSet)))
        map_after_infected_update = {}
        if len(infectedSet) < treshhold*numOfCreature:
            map_after_infected_update = simInfected(oldSimMap, probOfInfectHigh)
        else:
            map_after_infected_update = simInfected(oldSimMap, probOfInfectLow)
        map_status_next_gen = simNextGeneration(oldSimMap, map_after_infected_update, numOfGenToRecovery)
        oldSimMap = simMoveStep(map_status_next_gen).copy()
        Z = np.zeros([nrows, ncols])
        show_board(Z, w, win)
        time.sleep(0.01)
        #print(choices(isSickList,weights=(probOfInfectOne,1-probOfInfectOne),k=1))

def get_parameters():
    # num = e1.get()
    numOfCreatures = 10000
    percentageOfSick = 0.0001
    percentageOfHyper = 0.2
    NumOfGenToRecovery = 10
    probOfInfectHigh = 0.1
    probOfInfectLow = 0.05
    threshold = 0.5
    coronaSimulation(numOfCreatures, percentageOfSick, percentageOfHyper, NumOfGenToRecovery, probOfInfectHigh, probOfInfectLow, threshold)



def get_wide_pixels(Z, x, y, color, size):

    start = x * size
    end = y * size
    for i in range(start, start + size):
        for j in range(end, end + size):
            Z[i][j] = color

def show_board(Z, w, win):

    for regular in regularCreaturesSet:
        get_wide_pixels(Z, regular[0], regular[1], 1, 4)

    for sick in infectedSet:
        get_wide_pixels(Z, sick[0], sick[1], 2, 4)

    for recover in recoverSet:
        get_wide_pixels(Z, recover[0], recover[1], 3, 4)

    w.pack()
    if len(recoverSet) == 0:
        plt.imsave('check.png', Z, cmap=c_map_rec_empty)
    else:
        plt.imsave('check.png', Z, cmap=c_map_stn)

    img = ImageTk.PhotoImage(Image.open('check.png'))
    w.create_image(20, 20, anchor=NW, image=img)
    win.update_idletasks()
    win.update()

# parent = Tk()
# parent.geometry("300x400")
# user_input = StringVar(parent)
# name = Label(parent, text="Name").grid(row=0, column=0)
# e1 = Entry(parent)
# e1.grid(row=0, column=1)
# password = Label(parent, text="Password").grid(row=1, column=0)
# e2 = Entry(parent, textvariable=user_input)
# e2.grid(row=1, column=1)
# submit = Button(parent, text="Submit", command=get_parameters).grid(row=4, column=0)
# parent.mainloop()

numOfCreatures = 10000
percentageOfSick = 0.01
percentageOfHyper = 0.2
NumOfGenToRecovery = 10
probOfInfectHigh = 0.1
probOfInfectLow = 0.05
threshold = 0.5
coronaSimulation(numOfCreatures, percentageOfSick, percentageOfHyper, NumOfGenToRecovery, probOfInfectHigh,
                 probOfInfectLow, threshold)