import matplotlib.pyplot as plt
import csv
import ast

#create empty axises
X = []
Y = []
#read the output file of the algorithm
with open('covid7000_dci_out.txt', 'r') as datafile:
    next(datafile)
    #seperate it by brackets
    plotting = csv.reader(datafile, delimiter='}')
      
    for row in plotting:
        X.append(row[0])
        Y.append(int(row[1]))
#plot it in bar format
plt.barh(X, Y)
plt.title('Supports of Transactions')
plt.xlabel('Support')
plt.ylabel('Transaction')
plt.show()

'''
file = open("dict.txt", "r")

contents = file.read()
dictionary = ast.literal_eval(contents)

file.close()

'''
