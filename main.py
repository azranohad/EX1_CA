from random import random, randrange, choice, choices

import numpy

from  creature import creature

def initCreatures(numOfCreature,percentageOfSick,percentageOfHyper):
    sim_map = {}
    regularCreaturesSet = set({})
    infectedSet = set({})
    size =200
    numOfSick = int(numOfCreature*percentageOfSick)
    numOfHyper = int(numOfCreature*percentageOfHyper)
    i = 0
    while i < numOfCreature:
        if i<numOfSick:
            newPoint = (randrange(size),randrange(size))
            #newPoint = (100, 100)
            if newPoint in sim_map.keys():
               i = i - 1
            else:
               sim_map[newPoint] = creature(False, 1)
               infectedSet.add(newPoint)
        else:
            newPoint = (randrange(size), randrange(size))
            #newPoint = (100, 100)
            if newPoint in sim_map.keys():
               i = i - 1
            else:
               sim_map[newPoint] = creature(False)
               regularCreaturesSet.add(newPoint)

        i = i+1

    sim_map_clone = sim_map.copy()
    for j in range(numOfHyper):
        hyperCreature = choice(list(sim_map_clone.keys()))
        sim_map[hyperCreature].hyper = True
        sim_map_clone.pop(hyperCreature)
    j = 1
    return sim_map, regularCreaturesSet, infectedSet

def simInfected(oldSimMap,simKeys,probOfInfect):
    halfNewSimMap = oldSimMap.copy()
    isSickList = [0, 1]
    for key in simKeys:
        if oldSimMap[key].infected > 0:
            j = -1
            t = -1
            for j in range(-1, 2):
                for t in range(-1, 2):
                    if ((key[0] + j) % 200, (key[1] + t) % 200) in oldSimMap.keys() and (j != 0 or t != 0):
                        if choices(isSickList, weights=(1 - probOfInfect, probOfInfect), k=1)[0] == 1 and \
                                halfNewSimMap[(key[0] + j) % 200, (key[1] + t)].infected == 0:
                            halfNewSimMap[(key[0] + j) % 200, (key[1] + t)].infected = 1
    return halfNewSimMap

def coronaSimulation(numOfCreature,percentageOfSick,percentageOfHyper,numOfGenToRecovery,probOfInfectOne,probOfInfectTwo,treshhold):
    oldSimMap = {}
    newSimState = {}
    recoverSet = {}
    oldSimMap, regularCreaturesSet, infectedSet = initCreatures(numOfCreature, percentageOfSick, percentageOfHyper)
    #show simulation
    isSickList = [0,1]
    for i in range(100):
        halfNewSimMap = oldSimMap.copy()
        simKeys = oldSimMap.keys()
        halfNewSimMap = simInfected(oldSimMap,simKeys,probOfInfectOne)
        """
        for key in simKeys:
            if oldSimMap[key].infected > 0:
                j = -1
                t = -1
                for j in range(-1,2):
                    for t in range(-1,2):
                        if ((key[0]+j) % 200 , (key[1]+t) % 200) in oldSimMap.keys() and (j != 0 or t !=0):
                           if choices(isSickList, weights=( 1 - probOfInfectOne,probOfInfectOne), k=1)[0] == 1 and halfNewSimMap[(key[0]+j) % 200 , (key[1]+t)].infected == 0:
                               bla =  halfNewSimMap[(key[0]+j) % 200 , (key[1]+t)]
                               halfNewSimMap[(key[0]+j) % 200 , (key[1]+t)].infected = 1
        """
        print(choices(isSickList,weights=(probOfInfectOne,1-probOfInfectOne),k=1))

def main():
    numOfCreatures = 3000
    percentageOfSick = 0.1
    percentageOfHyper = 0.1
    NumOfGenToRecovery = 3
    probOfInfectOne = 0.3
    probOfInfectTwo = 0.1
    treshhold =0.1
    coronaSimulation(numOfCreatures,percentageOfSick,percentageOfHyper,NumOfGenToRecovery,probOfInfectOne,probOfInfectTwo,treshhold)


if __name__ == '__main__':
    main()

