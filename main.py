import network
from termcolor import colored

if __name__ == '__main__':
    print(colored("Pebble Network Simulator\n", "red", attrs=["bold","dark","underline"]))
    network1 = network.PebbleNetwork(TotalNodes=12,  # 257
                                     PrimaryFanout=4,  # 64
                                     ConnLatencyMean=100,
                                     ConnLatencyStd=30,
                                     BadActorPercentage=33)
    Cycles = 7
    MinTransactionsAtTime = 2
    MaxTransactionsAtTime = 7

    network1.GenerateTransactions(Cycles, MinTransactionsAtTime, MaxTransactionsAtTime)
    network1.ShowNetwork()  # Prints the network nodes for now.

