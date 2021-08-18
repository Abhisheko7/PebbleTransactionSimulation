import hashlib
import math
import random
import time

import numpy as np

import node
import nodesDivision

from termcolor import colored


class PebbleNetwork:
    """Initializes a Pebble Network with Given Parameters"""

    def __init__(self, TotalNodes, PrimaryFanout, ConnLatencyMean, ConnLatencyStd, BadActorPercentage):
        super(PebbleNetwork, self).__init__()
        self.TotalNodes = TotalNodes
        self.PrimaryFanout = PrimaryFanout
        self.ConnLatencyMean = ConnLatencyMean
        self.ConnLatencyStd = ConnLatencyStd
        self.BadActorPercentage = (float(BadActorPercentage) / float(100))
        self.NodeList = []
        self.CurrentTransactionHashList = []
        self.BadNodeIndexes = random.sample(range(self.TotalNodes),
                                            math.floor((self.BadActorPercentage * self.TotalNodes)))
        self.ConnLatencies = np.random.normal(self.ConnLatencyMean, self.ConnLatencyStd, self.TotalNodes)
        for i in range(self.TotalNodes):
            if i in self.BadNodeIndexes:
                self.NodeList.append(node.PebbleNode(True, self.ConnLatencies[i], self.TotalNodes))
            else:
                self.NodeList.append(node.PebbleNode(False, self.ConnLatencies[i], self.TotalNodes))
        self.NodesInNetwork = []  # This order is considered for the index position of the nodes in the vectorclock
        for i in range(self.TotalNodes):
            self.NodesInNetwork.append(self.NodeList[i].PublicKey)
        self.VectorClock = [0] * self.TotalNodes
        self.PrimeClock = []
        self.SecondaryClock = []
        self.TernaryClock = []
        self.TransactionHashList = []
        self.NowPrimaryNodeIndices = []
        self.NowSecondaryNodeIndices = []
        self.NowTernaryNodeIndices = []
        self.Timestamps = []

    def GenerateTransactions(self, LoopsNumber, MinTransAtTime, MaxTransAtATime):
        for i in range(LoopsNumber):
            transNowCount = random.randint(MinTransAtTime, MaxTransAtATime)
            print(
                colored(f"Num of transactions in cycle -- {i + 1} are -- {transNowCount} \n", "cyan", attrs=["bold", "dark"]))

            for j in range(transNowCount):
                self.CurrentTransactionHashList.append(
                    hashlib.md5(str(i + j + i * j * j * time.time()).encode("utf-8")).hexdigest())
            self.Simulation(self.CurrentTransactionHashList)
            self.CurrentTransactionHashList = []
            sec = 1
            time.sleep(sec)

    def SetPrimaryClock(self):
        self.PrimeClock = [None] * len(self.NowPrimaryNodes)

    def SetSecondaryClock(self):
        for i in range(len(self.NowPrimaryNodes)):
            self.List = [None] * len(self.NowSecondaryNodes[i])
            self.SecondaryClock.append(self.List)

    def SetTernaryClock(self):
        for i in range(len(self.NowPrimaryNodes)):
            self.list = [] * len(self.NowSecondaryNodes[i])
            for j in range(len(self.NowSecondaryNodes[i])):
                self.innerlist = [None] * len(self.NowTernaryNodes[i][j])
                self.list.append(self.innerlist)
            self.TernaryClock.append(self.list)

    def Simulation(self, TransactionHashList):
        self.Timestamps = []
        self.TransactionHashList = TransactionHashList
        self.NodeDivisionObj = nodesDivision.NodesDivision(self.TransactionHashList, self.TotalNodes,
                                                           self.PrimaryFanout,
                                                           self.NodeList)
        self.NodeDivisionObj.DivideTheNodes()
        self.NowPrimaryNodes = self.NodeDivisionObj.NowPrimaryNodes
        self.NowSecondaryNodes = self.NodeDivisionObj.NowSecondaryNodes
        self.NowTernaryNodes = self.NodeDivisionObj.NowTernaryNodes
        self.NowPrimaryNodeIndices = self.NodeDivisionObj.NowPrimaryNodeIndices
        self.NowSecondaryNodeIndices = self.NodeDivisionObj.NowSecondaryNodeIndices
        self.NowTernaryNodeIndices = self.NodeDivisionObj.NowTernaryNodeIndices
        self.SetPrimaryClock()
        self.SetSecondaryClock()
        self.SetTernaryClock()
        self.PrimeClock = self.PrimaryPropagation(self.NowPrimaryNodeIndices)
        self.SecondaryClock = self.SecondaryPropagation(self.PrimeClock, self.NowSecondaryNodeIndices)
        self.TernaryClock = self.TernaryPropagation(self.PrimeClock, self.SecondaryClock, self.NowTernaryNodeIndices)
        self.DisplayIndividualTransaction()

    def PrimaryPropagation(self, PrimaryIndices):
        self.SetPrimaryClock()
        for i in range(len(PrimaryIndices)):
            self.Id = self.NodeList[PrimaryIndices[i]].PublicKey
            self.PrimeClock[i] = tuple(
                self.NodeList[PrimaryIndices[i]].SendTransaction(self.NodesInNetwork.index(self.Id)))
        return self.PrimeClock

    def SecondaryPropagation(self, PrimeClock, SecondaryIndices):
        self.SetSecondaryClock()
        for i in range(len(PrimeClock)):
            for j in range(len(SecondaryIndices[i])):
                indice = SecondaryIndices[i][j]
                self.Id = self.NodeList[indice].PublicKey
                self.NodeList[indice].ReceiveTransaction(PrimeClock[i], self.NodesInNetwork.index(self.Id))
                self.SecondaryClock[i][j] = tuple(
                    self.NodeList[indice].SendTransaction(self.NodesInNetwork.index(self.Id)))
        return self.SecondaryClock

    def TernaryPropagation(self, PrimeClock, SecondaryClock, TernaryIndices):
        self.SetTernaryClock()
        for i in range(len(PrimeClock)):
            for j in range(len(SecondaryClock[i])):
                for k in range(len(TernaryIndices[i][j])):
                    indice = TernaryIndices[i][j][k]
                    self.Id = self.NodeList[indice].PublicKey
                    self.TernaryClock[i][j][k] = tuple(self.NodeList[indice].ReceiveTransaction(SecondaryClock[i][j],
                                                                                                self.NodesInNetwork.index(
                                                                                                    self.Id)))
            self.Timestamps.append(self.AnnounceFinalTimestamps(i))
        return self.TernaryClock

    def DisplayIndividualTransaction(self):
        for i in range(len(self.TransactionHashList)):
            transaction = self.TransactionHashList[i]
            print(colored(f"For transaction -\t{transaction}", "green",attrs=["bold","dark"]))
            print("Primary Node   \t\t", self.NowPrimaryNodes[i])
            print("Primary Node Index \t\t", self.NowPrimaryNodeIndices[i])
            print("Primary Clock \t\t ", self.PrimeClock[i])
            print("\nSecondary Nodes \t", self.NowSecondaryNodes[i])
            print("Secondary Node Indices \t\t", self.NowSecondaryNodeIndices[i])
            print("Secondary Clock \t", self.SecondaryClock[i])
            print("\nTernary Nodes \t\t", self.NowTernaryNodes[i])
            print("Ternary Node Indices \t\t", self.NowTernaryNodeIndices[i])
            print("Ternary CLock \t\t", self.TernaryClock[i])
            print("\n")
            print(colored(f"VECTOR TIMESTAMP ANNOUNCED - - {self.Timestamps[i]}", "magenta",
                          attrs=[ "bold", "dark"]))
            print("\n")

    def AnnounceFinalTimestamps(self, i):
        self.VectorClock = [0] * self.TotalNodes
        self.primeIndex = self.NowPrimaryNodeIndices[i]
        for j in range(len(self.NowSecondaryNodeIndices[i])):
            self.secIndex = self.NowSecondaryNodeIndices[i][j]
            for k in range(len(self.NowTernaryNodeIndices[i][j])):
                self.ternIndex = self.NowTernaryNodeIndices[i][j][k]
                for m in range(self.TotalNodes):
                    self.VectorClock[m] = max(self.VectorClock[m], self.NodeList[self.ternIndex].VectorTimestamps[m])
            for m in range(self.TotalNodes):
                self.VectorClock[m] = max(self.VectorClock[m], self.NodeList[self.secIndex].VectorTimestamps[m])
        for m in range(self.TotalNodes):
            self.VectorClock[m] = max(self.VectorClock[m], self.NodeList[self.primeIndex].VectorTimestamps[m])
        return self.VectorClock

    def ShowNetwork(self):
        for i in self.NodeList:
            print(colored("PublicKey: ","grey", attrs= ["bold"]), i.PublicKey, colored("\t\tNode ConnLatency: ", "grey", attrs= ["bold"]), i.connLatency, colored("\t\tBad Actor: ", "grey", attrs= ["bold"]), i.BadActor, "\t\t",
                  i.VectorTimestamps)
