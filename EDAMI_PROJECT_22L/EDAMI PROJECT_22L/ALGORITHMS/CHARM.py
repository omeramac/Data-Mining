
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from copy import copy
import pandas as pd
from time import process_time
import argparse
import dci_test as dci


class ProcessData:
    transactional = []
    tid_count = 0

    def import_data(self, filename):
        with open(filename, 'r') as file:
            tid = 1
            for line in file:
                line = line.strip().split()
                for element in line:
                    self.transactional.append({'tid': tid, 'item': element})
                tid += 1
        self.tid_count = tid - 1

    def transform_data(self):
        df = pd.DataFrame(self.transactional)
        self.itemsGrouped = df.groupby(['item'])['tid'].apply(list)
        self.itemsGrouped = pd.DataFrame({'item': self.itemsGrouped.index, 'tid': self.itemsGrouped.values})
        self.itemsGrouped['item'] = self.itemsGrouped['item'].apply(lambda x: {x})

    def get_frequent_items(self, min_sup):
        return self.itemsGrouped[self.itemsGrouped['tid'].map(len) >= min_sup * self.tid_count]


class CharmAlgorithm:
    def __init__(self, min_sup_config, tid_count):
        self.result = pd.DataFrame(columns=['item', 'tid', 'support'])
        self.min_sup = min_sup_config * tid_count

    @staticmethod
    def replace_values(df, column, find, replace):
        for row in df.itertuples():
            if find <= row[column]:
                row[column].update(replace)

    def charm_property(self, row1, row2, items, new_item, new_tid):
        if len(new_tid) >= self.min_sup:
            if set(row1[2]) == set(row2[2]):
                # remove row2[1] from items
                items = items[items['item'] != row2[1]]
                # replace all row1[1] with new_item
                find = copy(row1[1])
                self.replace_values(items, 1, find, new_item)
                self.replace_values(self.items_tmp, 1, find, new_item)
            elif set(row1[2]).issubset(set(row2[2])):
                # replace all row1[1] with new_item
                find = copy(row1[1])
                self.replace_values(items, 1, find, new_item)
                self.replace_values(self.items_tmp, 1, find, new_item)
            elif set(row2[2]).issubset(set(row1[2])):
                # remove row2[1] from items
                items = items[items['item'] != row2[1]]
                # add {item, tid} to self.items_tmp
                self.items_tmp = self.items_tmp.append({'item': new_item, 'tid': new_tid}, ignore_index=True)
                # sort items by ascending support
                # s = self.items_tmp.tid.str.len().sort_values().index
                # self.items_tmp = self.items_tmp.reindex(s).reset_index(drop=True)
            elif set(row1[2]) != set(row2[2]):
                # add {item, tid} to self.items_tmp
                self.items_tmp = self.items_tmp.append({'item': new_item, 'tid': new_tid}, ignore_index=True)

    def charm_extend(self, items_grouped):
        # sort items by ascending support
        s = items_grouped.tid.str.len().sort_values().index
        items_grouped = items_grouped.reindex(s).reset_index(drop=True)

        for row1 in items_grouped.itertuples():
            self.items_tmp = pd.DataFrame(columns=['item', 'tid'])
            for row2 in items_grouped.itertuples():
                if row2[0] >= row1[0]:
                    item = set()
                    item.update(row1[1])
                    item.update(row2[1])
                    tid = list(set(row1[2]) & set(row2[2]))
                    self.charm_property(row1, row2, items_grouped, item, tid)
            if not self.items_tmp.empty:
                self.charm_extend(self.items_tmp)
            # check if item subsumed
            is_subsumption = False
            for row in self.result.itertuples():
                if row1[1].issubset(row[1]) and set(row[2]) == set(row1[2]):
                    is_subsumption = True
                    break
            # append to result if element not subsumed
            if not is_subsumption:
                self.result = self.result.append({'item': row1[1], 'tid': row1[2], 'support': len(row1[2])},
                                                 ignore_index=True)

    def write_result_to_file(self, result_file):
        self.result.to_csv(result_file, sep='\t', columns=['item', 'support'], index=False)
        self.result.to_csv('graph.csv')


if __name__ == '__main__':

    def charm_algo(input,minisup,out):    
        # preparation
        data = ProcessData()
        data.import_data(input)
        data.transform_data()
        min_support = minisup
        #time_start = process_time()
        freq = data.get_frequent_items(min_support)

        # algorithm
        algorithm = CharmAlgorithm(min_support, data.tid_count)
        algorithm.charm_extend(freq)

        #end_time = process_time()
        # write to file

        algorithm.write_result_to_file(out)
        
        #print("Elapsed time for CHARM Algorithm:",end_time-time_start)


##################################################################################################################3
a = ['covid100.txt','covid1000.txt','covid5000.txt','covid7000.txt','covid10000.txt']
charm_outs = ['covid100_charm_out.txt','covid1000_charm_out.txt','covid5000_charm_out.txt','covid7000_charm_out.txt','covid10000_charm_out.txt']
dci_outs = ['covid100_dci_out.txt','covid1000_dci_out.txt','covid5000_dci_out.txt','covid7000_dci_out.txt','covid10000_dci_out.txt']
#charm_algo('covid100.txt',0.05,'covid100_charm_out')
#dci.dci_algo("covid100.txt",0.05,"covid100_dci_out")
dci_array = []
charm_array = []
minsuppp = 0.01

t=0
for i in a:
    print(type(i))
    file12 = open(i, 'r')
    con2 = len(file12.readlines())
    #con =sum(1 for line in d)
    print(con2)
    
    time_start2 = process_time()
    charm_algo(i,minsuppp,charm_outs[t])
    end_time2 = process_time()
    print("Elapsed time for CHARM Algorithm:",end_time2-time_start2)
    charm_array.append(end_time2-time_start2)
    t=t+1

print(charm_array)

k = 0
for d in a:
    print(type(d))
    file1 = open(d, 'r')
    con = len(file1.readlines())
    #con =sum(1 for line in d)
    print(con)
    dci_minsup =  minsuppp*con
    print(dci_minsup)
    time_start = process_time()
    dci.dci_algo(d,dci_minsup,dci_outs[k])
    end_time = process_time()
    print("Elapsed time for DCI_Closed Algorithm:",end_time-time_start)
    dci_array.append(end_time-time_start)
    k=k+1

print(dci_array)
#################################################################################3
import matplotlib.pyplot as plt

x = [100, 1000, 5000, 7000, 10000]
plt.plot(x, dci_array, label = "DCI_Closed")
plt.plot(x, charm_array, label = "CHARM")
plt.legend()
plt.show()
