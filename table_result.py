import networkx as nx
import numpy as np
import random
from math import pi, sqrt, log10

prefer_list = None
rank_list = None
allocation = None
available_set = None

def TTC(available_set):
    cycle_num = 0
    iter_num = 0
    G = nx.DiGraph()
    G.add_nodes_from(available_set)
    while available_set:
        # point to most prefer
        for i in available_set:
            # not point yet
            if G.out_degree(i) == 0:
                for j in prefer_list[i]:
                    if j in available_set:
                        G.add_edge(i, j)
                        break
        iter_num += 1
        for cycle in nx.simple_cycles(G):
            cycle_num += 1
            for i in range(-len(cycle), 0):   
                allocation[cycle[i]] = cycle[i+1]
                available_set.remove(cycle[i])
            G.remove_nodes_from(cycle)  
    
    return iter_num, cycle_num

n_parms = [i*50 for i in range(1,11)]
# from https://farter.cn/math/harmonic/
HarmonicSeries = {50:4.499205338329425, 100:5.187377517639621, 150:5.591180588643878, 200:5.878030948121444, 250:6.100675249432578, 300:6.282663880299503, 350:6.43657671054201, 400:6.569929691176507, 450:6.687573947254579, 500:6.792823429990524}

epoches = 500
iter_num = []
cycle_num = []
rank_sum = []

for n_parm in n_parms:
    prefer_list = [[i for i in range(n_parm)] for _ in range(n_parm)]
    rank_list = [[0]*n_parm for _ in range(n_parm)]
    iter_num.append(0)
    cycle_num.append(0)
    rank_sum.append(0)
    for _ in range(epoches):
        for i, j in zip(prefer_list, rank_list):
            random.shuffle(i)
            for h_i in range(n_parm):
                j[i[h_i]] = h_i
        allocation = [0]*n_parm
        available_set = set(np.arange(n_parm))
        res1, res2 = TTC(available_set)
        iter_num[-1] += res1
        cycle_num[-1] += res2
        rank_sum[-1] += sum(rank_list[i][allocation[i]] for i in range(n_parm))

iter_num = [i/epoches for i in iter_num]
cycle_num = [i/epoches for i in cycle_num]
rank_sum = [i/epoches for i in rank_sum]

for i in range(len(n_parms)):
    true_value = sqrt(8*n_parms[i]/pi)-3/pi*log10(n_parms[i])
    print(n_parms[i], f"{true_value:.2f}",f"{iter_num[i]:.2f}", f"{(iter_num[i]-true_value)/true_value*100:.2f}%", sep=" & ", end = " \\\\\n")

print()

for i in range(len(n_parms)):
    true_value = sqrt(2*n_parms[i]*pi)
    print(n_parms[i], f"{true_value:.2f}",f"{cycle_num[i]:.2f}", f"{(cycle_num[i]-true_value)/true_value*100:.2f}%", sep=" & ", end = " \\\\\n")

print()

for i in range(len(n_parms)):
    true_value = (n_parms[i]+1)*HarmonicSeries[n_parms[i]]-n_parms[i]
    print(n_parms[i], f"{true_value:.2f}",f"{rank_sum[i]+n_parms[i]:.2f}", f"{(rank_sum[i]+n_parms[i]-true_value)/true_value*100:.2f}%", sep=" & ", end = " \\\\\n")     
