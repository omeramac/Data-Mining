# -*- coding: utf-8 -*-
"""
Created on Fri May 20 12:01:35 2022

@author: Omer
"""


import numpy


                
#def createPostSet(dataBase, maxItemId, minSuppRelative):
    
 #   return numpy.array(postSet)

def isDup(newGenTIds, preset, dataBase):
    for i in preset:
        if(set(newGenTIds).issubset(set(dataBase[i]))):
            return True   
    return False

def intersectTIdSet(tIdSet1, tIdSet2):
    newTIdSet = []
    if(len(tIdSet1) > len(tIdSet2)):
        for tId in tIdSet2:
            if(numpy.any(tIdSet1 == tId)):
                newTIdSet.append(tId)
    else:
        for tId in tIdSet1:
            if(numpy.any(tIdSet2 == tId)):
                newTIdSet.append(tId)
    return numpy.array(newTIdSet)

def isSmallerAccordingToOrder(a, b, dataBase):
    if(a < b):
        return True
    else:
        return False

def isSmallerAccordingToSupport(a, b, dataBase):
    sizeA = len(dataBase[a])
    sizeB = len(dataBase[b])
    if(sizeA != sizeB):
        return sizeA < sizeB
    else:
        return isSmallerAccordingToOrder(a, b, dataBase)


#def sortPostSet(postSet, dataBase):        
              
#    return numpy.flip(postSet)     

def getSupport(item, dataBase):
    return len(dataBase[item])

def dci_closed(isFirstTime, closedSet, closedSetTIds, postSet, preSet, minSupp, dataBase, f_out):
    for i in postSet:
        newGenTIds = []

        if(isFirstTime):
            newGenTIds = dataBase[i]
        else:
            newGenTIds = intersectTIdSet(closedSetTIds, dataBase[i])
        
        if(len(newGenTIds) >= minSupp):
            newGen = numpy.append(closedSet, numpy.array([i]))

            if(isDup(newGenTIds, preSet, dataBase) == False):
                closedSetNew = numpy.array(newGen)

                if(isFirstTime):
                    closedNewTIds = dataBase[i]
                else:
                    closedNewTIds = numpy.array(newGenTIds)
                
                postSetNew = []

                for j in postSet:

                    if(isSmallerAccordingToSupport(i, j, dataBase)):

                        if(set(newGenTIds).issubset(dataBase[j])):
                            closedSetNew = numpy.append(closedSetNew, [j])

                            jTIds = dataBase[j]

                            closedNewTIds = intersectTIdSet(closedNewTIds, jTIds)
                        else:
                            postSetNew = numpy.append(postSetNew, [j])

                # print(numpy.sort(closedSetNew), len(closedNewTIds))
                f_out.write("{" + ' '.join(map(repr, closedSetNew.astype(int))) +  " } " + str(len(closedNewTIds)) + "\n")

                preSetNew = numpy.array(preSet)
                dci_closed(False, closedSetNew, closedNewTIds, postSetNew, preSetNew,  minSupp, dataBase, f_out)

                preSet = numpy.append(preSet, [i])

