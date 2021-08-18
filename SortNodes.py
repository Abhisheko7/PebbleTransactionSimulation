import random
from itertools import islice
from typing import List


class SortingNodes:
    def __init__(self, transaction, TotalNodes, PrimaryFanout, NodeList):
        super(SortingNodes, self).__init__()
        self.transactionHash = transaction[0:16]
        self.TotalNodes = TotalNodes
        self.PrimaryFanout = PrimaryFanout
        self.NodeList = NodeList
        self.transaction = ""
        self.PrimaryNode = ""
        self.NodesExcludingPrime = []
        self.SecondaryNodeIds = []
        self.TernaryNodesIds = []
        self.TernaryNodeIdsDivided = List[list]
        self.TernaryNodesDict = {}
        self.PublicKeysSorted = []
        self.PublicKeysShuffled = []
        self.ternaryNodesDivisionList = []
        self.NodesInOrder = []

    def PublicIdsDivision(self):
        random.seed(int(self.transactionHash, 16))
        randomIndices = list(range(self.TotalNodes))
        random.shuffle(randomIndices)
        totalTernaryNodes = self.TotalNodes - self.PrimaryFanout - 1
        y_int = totalTernaryNodes // self.PrimaryFanout
        y_addnl = totalTernaryNodes - y_int * self.PrimaryFanout
        for i in range(self.PrimaryFanout):
            self.TernaryNodesDict[i] = y_int
        for i in range(y_addnl):
            self.TernaryNodesDict[i] = self.TernaryNodesDict[i] + 1
        self.ternaryNodesDivisionList = list(self.TernaryNodesDict.values())
        for i in self.NodeList:
            self.PublicKeysSorted.append(i.PublicKey)
        self.PublicKeysSorted.sort()
        for i in randomIndices:
            self.PublicKeysSorted[i].replace('\'','')
            self.PublicKeysShuffled.append(self.PublicKeysSorted[i])
        random.seed(int(self.transactionHash[0:16], 16))
        self.PrimaryNode = random.choice(self.PublicKeysShuffled)
        self.NodesExcludingPrime = self.PublicKeysShuffled
        self.NodesExcludingPrime.remove(self.PrimaryNode)
        self.SecondaryNodeIds = self.NodesExcludingPrime[0:self.PrimaryFanout]
        self.TernaryNodesIds = self.NodesExcludingPrime[self.PrimaryFanout:]
        self.NodesInOrder.append(self.PrimaryNode)
        self.NodesInOrder.extend(self.NodesExcludingPrime)
        Input = iter(self.TernaryNodesIds)
        self.TernaryNodeIdsDivided = [list(islice(Input, elem)) for elem in self.ternaryNodesDivisionList]
        return self.PrimaryNode, self.SecondaryNodeIds, self.TernaryNodeIdsDivided
