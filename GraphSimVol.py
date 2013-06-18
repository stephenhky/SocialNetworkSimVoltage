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
        '''
        nodes = ['Stephen', 'Sinnie', 'Elaine']
        edges = [('Stephen', 'Sinnie', 0.2),
                 ('Sinnie', 'Stephen', 0.2),
                 ('Sinnie', 'Elaine', 0.3),
                 ('Elaine', 'Sinnie', 0.2),
                 ('Stephen', 'Elaine', 1.1),
                 ('Elaine', 'Stephen', 1.2)]
        '''
        nodes = ['Stephen', 'Sinnie']
        edges = [('Stephen', 'Sinnie', 0.54)]
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
            matB[edgeIdx, self.nodesIdx[edge[0]]] = 1
            matB[edgeIdx, self.nodesIdx[edge[1]]] = -1
        matB[len(self.edges), self.nodesIdx[node1]] = 1
        matB[len(self.edges), self.nodesIdx[node2]] = -1
        
        return matB
        
    def solveLinSystem(self, node1, node2, batteryVol=1.0):
        # vector: (currents, voltages, potentials)
        # # unknowns: (len(self.edges)+1, len(self.edges)+1, len(self.nodes)-2)
        matB = self.calculateIncidenceMatrix(node1, node2)
        # node1Idx = self.nodesIdx[node1]
        node2Idx = self.nodesIdx[node2]
        
        # square matrix
        ndim = 2 * len(self.edges) + len(self.nodes) + 1
        matM = np.matrix(np.zeros([ndim, ndim]))
        vecb = np.zeros(ndim)
        
        # B*I = 0  (excluding the grounded node)
        # number of eqns: len(self.nodes)-1
        for i in range(len(self.nodes)-1):
            for j in range(len(self.edges)+1):
                matM[i, j] = matB[j, i]
                
        # BP-V = 0  (including the battery)
        # number of eqns: len(self.edges)+1
        for di in range(len(self.edges)+1):
            i = len(self.nodes) - 1 + di
            if di != len(self.edges):
                j = len(self.edges) + 1 + di
                matM[i, j] = -1.
            else:
                vecb[len(self.nodes) + len(self.edges) - 1] = -1.
            for dj in range(len(self.nodes)):
                if dj != node2Idx:
                    j = 2 * len(self.edges) + 1 + dj
                    j -= 1 if dj > node2Idx else 0
                    matM[i, j] = matB[di, dj]
                    
        # IR-V = 0   (including the battery)
        # number of eqns: len(self.edges)+1
        for di in range(len(self.edges)):
            i = len(self.nodes) + len(self.edges) + di
            ij = di
            vj = len(self.edges) + 1 + di
            matM[i, ij] = self.edges[di][2]
            matM[i, vj] = -1.
        matM[ndim-1, len(self.edges)] = 1.
        matM[ndim-1, ndim-1] = -batteryVol
        
        return np.array(matM), vecb
        
    def getResistance(self, node1, node2):
        matM, vecb = self.solveLinSystem(node1, node2)
        vecX = np.linalg.solve(matM, vecb)
        return 1/vecX[-1]
