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
        
        return matB
        
    def solveLinSystem(self, node1, node2):
        # vector: (currents, voltages, potentials)
        # # unknowns: (len(self.edges)+1, len(self.edges)+1, len(self.nodes)-2)
        matB = self.calculateIncidenceMatrix(node1, node2)
        node1Idx = self.nodesIdx[node1]
        node2Idx = self.nodesIdx[node2]
        
        # square matrix
        ndim = 2 * len(self.edges) + len(self.nodes)
        matM = np.matrix(np.zeros([ndim, ndim]))
        vecb = np.zeros(ndim)
        
        # B*I = 0
        # number of eqns: len(self.nodes)
        for i in range(len(self.nodes)):
            for j in range(len(self.edges)+1):
                matM[i, j] = matB[j, i]
                
        # BP-V = 0
        # number of eqns: len(self.edges)
        for i, di in zip(range(len(self.edges)), 
                         range(len(self.nodes), 
                               len(self.nodes)+len(self.edges))):
            matM[di, i+len(self.edges)+1] = -1.
            for j in range(len(self.nodes)):
                if j == node1Idx or j == node2Idx:
                    vecb[di] = matB[i, j] if j == node1Idx else 0
                else:
                    pjzero = 2 * len(self.edges) + 2
                    pj = pjzero + j
                    pj -= 1 if j > node1Idx else 0
                    pj -= 1 if j > node2Idx else 0
                    matM[di, pj] = matB[i, j]
                    
        # IR-V = 0
        # number of eqns: len(self.edges)
        for i in range(len(self.edges)):
            di = len(self.nodes) + len(self.edges) + i
            vi = len(self.edges) + 1 + i
            matM[di, i] = self.edges[i][2]
            matM[di, vi] = -1.
            
        return matM
        
