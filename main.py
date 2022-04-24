import time
from random import randrange, choice, choices

from tkinter import *
import numpy as np
from PIL import Image, ImageTk
from matplotlib import pyplot as plt, cm, colors
from matplotlib.colors import ListedColormap
from creature import creature
import random

master = Tk()
regularCreaturesSet = set()
infectedSet = set()
recoverSet = set()

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


def coronaSimulation(numOfCreatures,percentageOfSick,percentageOfHyper,numOfGenToRecovery,probOfInfectHigh,probOfInfectLow,treshhold):
    oldSimMap = initCreatures(numOfCreatures, percentageOfSick, percentageOfHyper)
    nrows = 800
    ncols = 800
    insulation = 0

    for i in range(10000):
        if len(infectedSet) == 0:
            break
        map_after_infected_update = {}
        if len(infectedSet) > treshhold*numOfCreatures:
            insulation = numOfGenToRecovery*0.4
        if insulation > 0:
            map_after_infected_update = simInfected(oldSimMap, probOfInfectLow)
            insulation -= 1
        else:
            map_after_infected_update = simInfected(oldSimMap, probOfInfectHigh)
        map_status_next_gen = simNextGeneration(oldSimMap, map_after_infected_update, numOfGenToRecovery)
        oldSimMap = simMoveStep(map_status_next_gen).copy()
        Z = np.zeros([nrows, ncols])
        show_board(Z)
        time.sleep(0.02)

def get_wide_pixels(Z, x, y, color, size):

    start = x * size
    end = y * size
    for i in range(start, start + size):
        for j in range(end, end + size):
            Z[i][j] = color

def show_board(Z):

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


parent = Tk()
parent.geometry("350x200")
user_input = StringVar(parent)
numOfCreaturesLabel = Label(parent, text="Number Of Creatures").grid(row=0, column=0)

numOfCreatures = Entry(parent)
numOfCreatures.grid(row=0, column=1)
percentageOfSickLabel = Label(parent, text="Percentage Of Sick").grid(row=1, column=0)
percentageOfSick = Entry(parent)
percentageOfSick.grid(row=1, column=1)
percentageOfHyperLabel = Label(parent, text="Percentage Of Hyper").grid(row=2, column=0)
percentageOfHyper = Entry(parent)
percentageOfHyper.grid(row=2, column=1)
NumOfGenToRecoveryLabel = Label(parent, text="Number Of Generation To Recovery").grid(row=3, column=0)
NumOfGenToRecovery = Entry(parent)
NumOfGenToRecovery.grid(row=3, column=1)
probOfInfectHighLabel = Label(parent, text="probability Of Infect High").grid(row=4, column=0)
probOfInfectHigh = Entry(parent)
probOfInfectHigh.grid(row=4, column=1)
probOfInfectLowLabel = Label(parent, text="probability Of Infect Low").grid(row=5, column=0)
probOfInfectLow = Entry(parent)
probOfInfectLow.grid(row=5, column=1)
thresholdLabel = Label(parent, text="threshold").grid(row=6, column=0)
threshold = Entry(parent)
threshold.grid(row=6, column=1)
submit = Button(parent, text="Submit", command=lambda:[parent.quit()]).grid(row=7, column=0)

parent.mainloop()
win = Tk()
w = Canvas(master, width=1000, height=800, bg="white")
coronaSimulation(int(numOfCreatures.get()), float(percentageOfSick.get()),float(percentageOfHyper.get()),int(NumOfGenToRecovery.get()),
                 float(probOfInfectHigh.get()),float(probOfInfectLow.get()),float(threshold.get()))


