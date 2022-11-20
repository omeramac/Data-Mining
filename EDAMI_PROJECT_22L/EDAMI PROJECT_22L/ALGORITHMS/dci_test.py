
import DCI_closed as dci
from time import process_time
import numpy as np

#enter the minsup value here
min_supp_convert = 0.05  #<<== HERE
size_of_data = 7000
minSupp = size_of_data*min_supp_convert
dataBase = {}
#maxItemId = dci.readDataFromFileToDataBase(dataBase, "covid1000.txt")
file_dci = open("covid7000.txt", "r")
nTId = 0
maxItemId = 0
for i in file_dci.readlines():
    nTId += 1
    lineSplitted = i.split()
    for value in lineSplitted:
        item = int(value)
        if(item in dataBase):
            dataBase[item] = np.append(dataBase[item], nTId)
        else:
            dataBase[item] = np.array([nTId])
        if(item > maxItemId):
            maxItemId = item

file_dci.close()

#print(maxItemId)
#postSet = dci.createPostSet(dataBase, maxItemId, minSupp)

postSet = []
for i in range(1, maxItemId + 1):
    try:
        tidSet = dataBase[i]
    except:
        continue
    if(len(tidSet) >= minSupp):
        postSet.append(i)
#print(postSet)
# print(postSet)
#postSet = dci.sortPostSet(postSet, dataBase)

for i in range(len(postSet)):
        minimum = i       
        for j in range(i + 1, len(postSet)):
            if(dci.isSmallerAccordingToSupport(postSet[minimum], postSet[j], dataBase)):
                minimum = j
        postSet[minimum], postSet[i] = postSet[i], postSet[minimum]
postSet = np.flip(postSet)        

##########33
closedSet = []
closedSetTIds = []
preSet = []

# print(postSet)
# for i in postSet:
    # print(getSupport(i, dataBase))
f_out = open("covid7000_dci_out.txt","w")
time_start = process_time()
dci.dci_closed(True, closedSet, closedSetTIds, postSet, preSet, minSupp, dataBase, f_out)
end_time = process_time()
f_out.close()

print("Elapsed time for DCI_closed Algorithm:",end_time-time_start)