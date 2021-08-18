import SortNodes


class NodesDivision:
    def __init__(self, transactionHashList, TotalNodes, PrimaryFanout, NodeList):
        self.transactionList = transactionHashList
        self.TotalNodes = TotalNodes
        self.PrimaryFanout = PrimaryFanout
        self.NodeList = NodeList
        self.SortedNodes = []
        self.NowPrimaryNodes = []
        self.NowSecondaryNodes = []
        self.NowTernaryNodes = []
        self.NowPrimaryNodeIndices = []
        self.NowSecondaryNodeIndices = []
        self.NowTernaryNodeIndices = []

    def AssignIndices(self):
        for i in range(len(self.NowPrimaryNodes)):
            for node in self.NodeList:
                if node.PublicKey == self.NowPrimaryNodes[i]:
                    self.NowPrimaryNodeIndices[i] = self.NodeList.index(node)
            for j in range(len(self.NowSecondaryNodes[i])):
                for node in self.NodeList:
                    if node.PublicKey == self.NowSecondaryNodes[i][j]:
                        self.NowSecondaryNodeIndices[i][j] = self.NodeList.index(node)
                for k in range(len(self.NowTernaryNodes[i][j])):
                    for node in self.NodeList:
                        if node.PublicKey == self.NowTernaryNodes[i][j][k]:
                            self.NowTernaryNodeIndices[i][j][k] = self.NodeList.index(node)

    def DivideTheNodes(self):
        for transaction in self.transactionList:
            self.SortedNodes.append(SortNodes.SortingNodes(transaction, self.TotalNodes, self.PrimaryFanout, self.NodeList))
        for SortNodeObj in self.SortedNodes:
            self.PrimaryNode, self.SecondaryNodes, self.TernaryNodes = SortNodeObj.PublicIdsDivision()
            self.NowPrimaryNodes.append(self.PrimaryNode)
            self.NowSecondaryNodes.append(self.SecondaryNodes)
            self.NowTernaryNodes.append(self.TernaryNodes)
            self.NowPrimaryNodeIndices = [None] * len(self.NowPrimaryNodes)
        for i in range(len(self.NowPrimaryNodes)):
            self.list = [] * len(self.NowSecondaryNodes[i])
            self.List = [None] * len(self.NowSecondaryNodes[i])
            self.NowSecondaryNodeIndices.append(self.List)
            for j in range(len(self.NowSecondaryNodes[i])):
                self.innerlist = [None] * len(self.NowTernaryNodes[i][j])
                self.list.append(self.innerlist)
            self.NowTernaryNodeIndices.append(self.list)
        self.AssignIndices()





