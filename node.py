import hashlib
import time


class PebbleNode:
    """Initializes a Pebble Node with Given parameters"""

    def __init__(self, badActor, connLatency, TotalNodesInNetwork):
        super(PebbleNode, self).__init__()
        self.BadActor = badActor
        self.connLatency = connLatency
        self.TotalNodes = TotalNodesInNetwork
        self.VectorTimestamps = [0] * TotalNodesInNetwork
        self.PublicKey = hashlib.md5(str(self.connLatency + time.time()).encode("utf-8")).hexdigest()

    def LocalUpdates(self, MyIndex):
        self.VectorTimestamps[MyIndex] += 1
        return self.VectorTimestamps

    def SendTransaction(self, MyIndex):
        self.VectorTimestamps[MyIndex] += 1
        return self.VectorTimestamps

    def ReceiveTransaction(self, SenderVector, MyIndex):
        for i in range(self.TotalNodes):
            self.VectorTimestamps[i] = max(self.VectorTimestamps[i], SenderVector[i])
        self.VectorTimestamps[MyIndex] += 1
        '''time.sleep(self.connLatency)  # Sleeping for simulate connection latency.
        if self.BadActor:
            pass  # TODO: Show Malicious Behaviour when it receives a transaction
        else:'''
        return self.VectorTimestamps
