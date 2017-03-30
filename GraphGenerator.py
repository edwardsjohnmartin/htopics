import networkx as nx
import matplotlib.pyplot as plotter
from normalizr import Normalizr
from collections import Counter

normalizr = Normalizr(language='en')
graph = nx.Graph()

fileName = "user tweets.txt"
historyData = set()
#historyFile = open("HistoryData.txt", 'r')
historyFile = open(fileName, 'r')
historyData = historyFile.readlines()

print(historyData)

readFile = open(fileName, 'r')
stringList = []
content = readFile.readlines()

numWords = 0
minEdgeWeight = 1

edgeWeightList = []
sumEdgeWeight = 0

print(len(content))

bannedWords = ["", "rt", "amp"]
for x in range(0, len(content)):
    stringList.append([])
    stringList[x] = content[x].split(" ")
            
for x in range(0, len(content)):
    tweetWords = stringList[x]
    numWords = len(tweetWords)
    for i in range (0, numWords):
        word = normalizr.normalize(stringList[x][i].lower())
        stringList[x][i] = word
    for i in range(0, numWords):
        firstWord = stringList[x][i]
        for j in range(i+1, numWords):
            secondWord = stringList[x][j]
            if graph.has_edge(firstWord, secondWord):
                updatedWeight = graph[firstWord][secondWord]['weight'] + 1
                graph.add_edge(firstWord, secondWord, weight=updatedWeight)
            elif (firstWord not in bannedWords) and (secondWord not in bannedWords):
                graph.add_edge(firstWord, secondWord, weight=minEdgeWeight)

edgeList = graph.edges()

for edge in edgeList:
    dict = graph.get_edge_data(*edge)
    edgeWeight = dict['weight']
    edgeWeightList.append(edgeWeight)
    sumEdgeWeight = sumEdgeWeight + edgeWeight

data = Counter(edgeWeightList)
modes = data.most_common()
averageEdgeWeight = sumEdgeWeight/len(edgeList)
print("Modes of edge weight (including their frequency):\r\n" + str(modes))
print("Edge weight average: " + str(int(averageEdgeWeight)))
  
desiredEdgeWeight = int(input("Minimum weight of edges:\r\n"))
for node in graph.nodes():
    nodeNeighbors = graph.neighbors(node)
    numNeighbors = len(nodeNeighbors)
    for i in range(0, numNeighbors):
        dict = graph.get_edge_data(node, nodeNeighbors[i])
        edgeWeight = dict['weight']
        if edgeWeight < desiredEdgeWeight:
            graph.remove_edge(node, nodeNeighbors[i])

for node in graph.nodes():
    if (len(graph.neighbors(node)) == 0):
        graph.remove_node(node)
        
nx.draw(graph, with_labels = True, node_size=1000, node_color="g", font_size=10)
plotter.show()

