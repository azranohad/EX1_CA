from random import randrange, choice, choices

import numpy as np
from matplotlib import pyplot as plt

from creature import creature
import random

regularCreaturesSet = set()
infectedSet = set()
recoverSet = set()
list_of_counts = []


def initCreatures(numOfCreature, percentageOfSick, percentageOfHyper):
    sim_map = {}
    size = 200
    numOfSick = int(numOfCreature*percentageOfSick)
    numOfHyper = int(numOfCreature*percentageOfHyper)
    i = 0
    while i < numOfCreature:
        if i < numOfSick:
            newPoint = (randrange(size), randrange(size))
            #newPoint = (100, 100)
            if newPoint in sim_map.keys():
               continue
            else:
               sim_map[newPoint] = creature(False, 1)
               infectedSet.add(newPoint)
        else:
            newPoint = (randrange(size), randrange(size))
            #newPoint = (100, 100)
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

def simInfected(oldSimMap, simKeys, probOfInfect):
    halfNewSimMap = oldSimMap.copy()
    isSickList = [0, 1]
    for key in simKeys:
        if oldSimMap[key].infected > 0:
            for x_step in range(-1, 2):
                for y_step in range(-1, 2):
                    if x_step == 0 and y_step == 0:
                        continue
                    neighbor_to_check = (key[0] + x_step) % 200, (key[1] + y_step) % 200
                    if neighbor_to_check in oldSimMap.keys():
                        if choices(isSickList, weights=(1 - probOfInfect, probOfInfect), k=1)[0] == 1 and \
                                halfNewSimMap[neighbor_to_check].infected == 0:
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
    # infectedSet.clear()
    # regularCreaturesSet.clear()
    # recoverSet.clear()
    for creature_point in oldMap.keys():

        new_point = get_new_point(creature_point, oldMap[creature_point].hyper)
        while new_point not in newMap.keys() and new_point not in oldMap.keys():
            new_point = get_new_point(creature_point, oldMap[creature_point].hyper)

        newMap[new_point] = oldMap[creature_point]
        if newMap[new_point].infected > 0:
            infectedSet.add(new_point)
        elif newMap[new_point].infected == 0:
            regularCreaturesSet.add(new_point)
        elif newMap[new_point].infected < 0:
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
    for i in range(100):
        list_of_counts.append((i, len(regularCreaturesSet), len(infectedSet), len(recoverSet)))
        halfNewSimMap = oldSimMap.copy()
        simKeys = oldSimMap.keys()
        if len(infectedSet) < treshhold*numOfCreature:
            simInfected(oldSimMap, simKeys, probOfInfectHigh)
        else:
            simInfected(oldSimMap, simKeys, probOfInfectLow)
        halfNewSimMap = simNextGeneration(oldSimMap, halfNewSimMap, numOfGenToRecovery)
        newList = simMoveStep(halfNewSimMap)
        #showList
        oldSimMap = newList.copy()
        #print(choices(isSickList,weights=(probOfInfectOne,1-probOfInfectOne),k=1))

def main():
    numOfCreatures = 16000
    percentageOfSick = 0.1
    percentageOfHyper = 0.3
    NumOfGenToRecovery = 10
    probOfInfectHigh = 0.6
    probOfInfectLow = 0.2
    threshold = 0.4
    show_board()
    coronaSimulation(numOfCreatures, percentageOfSick, percentageOfHyper, NumOfGenToRecovery, probOfInfectHigh, probOfInfectLow, threshold)
    x = 3

def show_board():
    board = np.zeros((200, 200))
    board[0, 0] = 0.5
    plt.imshow(board)
    plt.show()
    x = 3
if __name__ == '__main__':
    main()

