# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:24:00 2013

@author: Kwan-Yuet Ho, Ph.D.
"""

import networkx as nx

class SocialNetworkSimVoltage():
    def __init__(self):
        nodes = ['Stephen', 'Sinnie', 'Elaine']
        edges = [('Stephen', 'Sinnie', 0.2),
                 ('Sinnie', 'Stephen', 0.2),
                 ('Sinnie', 'Elaine', 0.3),
                 ('Elaine', 'Sinnie', 0.2),
                 ('Stephen', 'Elaine', 1.1),
                 ('Elaine', 'Stephen', 1.2)]
        self.initializeClass(nodes, edges)

    def initializeClass(self, nodes, edges):
        self.constructSocialNetwork(nodes, edges)
        self.errTol = 1e-4
        self.maxSteps = 10000

    def constructSocialNetwork(self, nodes, edges):
        self.wordNet = nx.DiGraph()
        for node in nodes:
            self.wordNet.add_node(node)
        self.wordNet.add_weighted_edges_from(edges)
        #for edge in edges:
        #    self.wordNet.add_edge(*edge)  

    def checkPersonIrrelevantClumsy(self, person, person1, person2):
        all_paths = nx.algorithms.all_simple_paths(self.wordNet, person1, 
                                                   person2, weight='weight')
        for path in all_paths:
            if (person in path):
                return False
        return True
        
    def checkPersonIrrelevant(self, person, person1, person2):
        path1 = nx.algorithms.shortest_path(self.wordNet,
                                           source = person1, target = person,
                                           weight='weight')
        path2 = nx.algorithms.shortest_path(self.wordNet,
                                           source = person, target = person2,
                                           weight='weight')
        #print path1, path2
        intersection_paths = list(set(path1) & set(path2))
        #print intersection_paths
        return (len(intersection_paths) != 1)
    
    def getResistance(self, person1, person2, printVol = False):
        if person1 == person2:
            return 0.0
        try:
            distTwoWords = self.getShortestDist(person1, person2)
        except nx.exception.NetworkXNoPath:
            return float('inf')
        
        volDict = {}
        for node in self.wordNet:
            if node == person1:
                volDict[node] = 1.0
            elif node == person2:
                volDict[node] = 0.0
            else:
                if self.checkPersonIrrelevant(node, person1, person2):
                    volDict[node] = 10.0
                else:
                    distFrom1 = float(self.getShortestDist(person1, node))
                    distFrom2 = float(self.getShortestDist(node, person2))
                    volDict[node] = distFrom2 / (distFrom1 + distFrom2)
        tempVolDict = {}
        for node in self.wordNet:
            tempVolDict[node] = volDict[node]
            
        converged = False
        step = 0
        while (not converged) and step < self.maxSteps:
            tempConverged = True
            for node in self.wordNet:
                if node == person1:
                    tempVolDict[node] = 1.0
                elif node == person2:
                    tempVolDict[node] = 0.0
                elif (volDict[node] < 0.0) or (volDict[node] > 1.0):
                    tempVolDict[node] = 10.0
                else:
                    predNodes = self.wordNet.predecessors(node)
                    succNodes = self.wordNet.successors(node)
                    in_current = 0.0
                    out_current = 0.0
                    for pred in predNodes:
                        if (volDict[pred] >= 0.0) and (volDict[pred] <= 1.0):
                            if volDict[pred] > volDict[node]:
                                potDiff = volDict[pred] - volDict[node]
                                resEdge = self.wordNet[pred][node]['weight']
                                in_current += potDiff / resEdge
                    for succ in succNodes:
                        if (volDict[succ] >= 0.0) and (volDict[succ] <= 1.0):
                            if volDict[node] > volDict[succ]:
                                potDiff = volDict[node] - volDict[succ]
                                resEdge = self.wordNet[node][succ]['weight']
                                out_current += potDiff
                    if abs(in_current - out_current) > self.errTol:
                        sumVOverR = 0.0
                        numRecR = 0
                        for pred in predNodes:
                            if (volDict[pred]>=0.0) and (volDict[pred]<=1.0):
                                if volDict[pred] > volDict[node]:
                                    resEdge = self.wordNet[pred][node]['weight']
                                    sumVOverR += volDict[pred] / resEdge
                                    numRecR += 1. / resEdge
                        for succ in succNodes:
                            if (volDict[succ]>=0.0) and (volDict[succ]<=1.0):
                                if volDict[node] > volDict[succ]:
                                    resEdge = self.wordNet[node][succ]['weight']
                                    sumVOverR += volDict[succ] / resEdge
                                    numRecR += 1. /resEdge
                        if numRecR == 0:
                            tempVolDict[node] = 0.0
                        else:
                            tempVolDict[node] = sumVOverR / numRecR
                        tempConverged = False
                    else:
                        tempConverged = tempConverged and True
            converged = tempConverged
            for node in self.wordNet:
                volDict[node] = tempVolDict[node]
            step += 1
            if printVol:
                print volDict

        startCurrent = 0.0        
        for rootsucc in self.wordNet.successors(person1):
            if volDict[rootsucc] <= 1.0:
                resEdge = self.wordNet[person1][rootsucc]['weight']
                startCurrent += (1.0 - volDict[rootsucc]) / resEdge
        return (1.0 / startCurrent)
                                
    def drawNetwork(self):
        nx.draw(self.wordNet)
        
    def getShortestDist(self, person1, person2):
        return nx.shortest_path_length(self.wordNet, person1, person2,
                                       weight='weight')
        
class StephenWordNetworkSimVoltage(SocialNetworkSimVoltage):
    def __init__(self):
        nodes = ['Stephen', 'John', 'Mary',
                 'Joshua',
                 'Abigail', 'Andrew', 'Jacob', 'Melanie',
                 'Shirley', 'Zoe', 'Wallace', 'Susan',
                 'Urban']
        edges = [('Stephen', 'Jacob', 1),
                 ('Jacob', 'Stephen', 1),
                 ('Stephen', 'Abigail', 1), 
                 ('Abigail', 'Stephen', 1),
                 ('Stephen', 'Andrew', 1),
                 ('Andrew', 'Stephen', 1),
                 ('Andrew', 'Abigail', 1),
                 ('Abigail', 'Andrew', 1),
                 ('John', 'Stephen', 1),
                 ('Andrew', 'John', 1),
                 ('John', 'Andrew', 1),
                 ('Abigail', 'John', 1), 
                 ('John', 'Abigail', 1),
                 ('John', 'Mary', 1),
                 ('Mary', 'John', 1),
                 ('John', 'Joshua', 1),
                 ('Joshua', 'John', 1),
                 ('John', 'Jacob', 1),
                 ('Jacob', 'John', 1),
                 ('Abigail', 'Jacob', 1),
                 ('Jacob', 'Abigail', 1),
                 ('Jacob', 'Andrew', 1),
                 ('Andrew', 'Jacob', 1),
                 ('Shirley', 'Stephen', 1),
                 ('Stephen', 'Shirley', 1),
                 ('Melanie', 'Stephen', 1),
                 ('Stephen', 'Melanie', 1),
                 ('Melanie', 'Shirley', 1),
                 ('Shirley', 'Urban', 1),
                 ('Urban', 'Shirley', 1),
                 ('Susan', 'Shirley', 1),
                 ('Shirley', 'Susan', 1),
                 ('Shirley', 'Zoe', 1),
                 ('Zoe', 'Shirley', 1),
                 ('Shirley', 'Wallace', 1),
                 ('Wallace', 'Shirley', 1),
                 ('Zoe', 'Wallace', 1)]
        self.initializeClass(nodes, edges)

def testrun():
    wn1 = StephenWordNetworkSimVoltage()
    for word in wn1.wordNet:
        resistance = wn1.getResistance('Stephen', word)
        print('Stephen -> %s : %.4f' % (word, resistance))
    for word in wn1.wordNet:
        resistance = wn1.getResistance(word, 'Stephen')
        print('%s -> Stephen : %.4f' % (word, resistance))
                                                             
if __name__ == '__main__':
    testrun()
