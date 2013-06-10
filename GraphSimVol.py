# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 10:03:42 2013

@author: hok1
"""

import numpy as np

class NodeNotExistException(Exception):
    def __init__(self, node):
        self.message = 'Node '+node+' does not exist!'

class GraphSimVoltage:
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
        self.nodes = nodes
        self.edges = edges
        
        self.nodesIdx = {}
        for idx in range(len(self.nodes)):
            self.nodesIdx[self.nodes[idx]] = idx
            
    def calculateIncidenceMatrix(self, node1, node2):
        if not (node1 in self.nodes):
            raise NodeNotExistException(node1)
        if not (node2 in self.nodes):
            raise NodeNotExistException(node2)
        
        matB = np.matrix(np.zeros([len(self.edges)+1, len(self.nodes)]))
        for edgeIdx in range(len(self.edges)):
            edge = self.edges[edgeIdx]
            matB[edgeIdx, self.nodesIdx[edge[0]]] = -1
            matB[edgeIdx, self.nodesIdx[edge[1]]] = 1
        matB[len(self.edges), self.nodesIdx[node1]] = -1
        matB[len(self.edges), self.nodesIdx[node2]] = 1
        
    def solveLinSystem(self, node1, node2):
        # vector: (currents, voltages, R, potentials)
        matB = self.calculateIncidenceMatrix(node1, node2)
        
        # square matrix
        matM = np.matrix()
