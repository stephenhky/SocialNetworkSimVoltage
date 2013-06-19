# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 11:28:52 2013

@author: hok1
"""

import SimVolGraph as svg
import weightedSocialNetworkSimVol as wsn
from itertools import permutations

nodes = ['Stephen', 'Sinnie', 'Elaine']
edges_uni = [('Stephen', 'Sinnie', 1),
             ('Sinnie', 'Elaine', 1.5),
             ('Stephen', 'Elaine', 1.2)]
             
edges_bi = []
for edge in edges_uni:
    reverse_edge = (edge[1], edge[0], edge[2])
    edges_bi.append(edge)
    edges_bi.append(reverse_edge)

iteralg = wsn.SocialNetworkSimVoltage()
iteralg.initializeClass(nodes, edges_bi)

gralg = svg.GraphSimVoltage()
gralg.initializeClass(nodes, edges_uni)

for node1, node2 in permutations(nodes, 2):
    print node1, ' -> ', node2, ' = ', iteralg.getResistance(node1, node2), '\t', gralg.getResistance(node1, node2)
    
'''
output:
Stephen  ->  Sinnie  =  0.72972972973   0.72972972973
Stephen  ->  Elaine  =  0.810810810811 	0.810810810811
Sinnie  ->  Stephen  =  0.72972972973 	0.72972972973
Sinnie  ->  Elaine  =  0.891891891892 	0.891891891892
Elaine  ->  Stephen  =  0.810810810811 	0.810810810811
Elaine  ->  Sinnie  =  0.891891891892 	0.891891891892
'''
