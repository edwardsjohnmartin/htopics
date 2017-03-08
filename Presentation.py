import networkx as nx
import matplotlib.pyplot as plotter
from normalizr import Normalizr
from collections import Counter

normalizr = Normalizr(language='en')

#Corpus variables
corpus = nx.Graph()
crpFileName = "us history timeline.txt"
crpFile = open(crpFileName, 'r')
crpLines = crpFile.readline()
crpLines = crpLines.split(" ")
crpLines = [str for str in crpLines if str != ""]
crpEdgeWeight = 1
capNodeWeight = 5
crpMaxX = len(crpLines)

neighborNum = int(input("Min num neighbors for each node (2 or more):\r\n"))

#Graph variables
graph = nx.Graph()
fileName = "a.txt"
historyData = set()
historyFile = open("a.txt", 'r')
historyData = historyFile.readlines()
readFile = open(fileName, 'r')
stringList = []
content = readFile.readlines()
numWords = 0
minEdgeWeight = 1
edgeWeightList = []
print(len(content))

#Creates the corpus----------------------------------------------------
for x in range(0, crpMaxX):  
    for y in range(1, min(neighborNum+1, (crpMaxX-x))):
        firstWord = crpLines[x]
        secondWord = crpLines[x+y]
        if (firstWord != secondWord):
            crpEdgeWeight = 1
            if (firstWord[0].isupper()):
                crpEdgeWeight = crpEdgeWeight + capNodeWeight
            if (secondWord[0].isupper()):
                crpEdgeWeight = crpEdgeWeight + capNodeWeight
                
            firstWord = firstWord.lower()
            secondWord = secondWord.lower()
                
            if corpus.has_edge(firstWord, secondWord):
                dict = corpus.get_edge_data(firstWord, secondWord)
                crpEdgeWeight = dict['weight']
                crpEdgeWeight = crpEdgeWeight * 2
            else:
                corpus.add_edge(firstWord, secondWord, weight=crpEdgeWeight)

crpEdgeList = corpus.edges()
crpEdgeWeightList = []
crpNodeList = corpus.nodes()

for edge in crpEdgeList:
    dict = corpus.get_edge_data(*edge)
    edgeWeight = dict['weight']
    edgeWeightList.append(edgeWeight)
#--------------------------------------------------------------------

bannedWords = ["", "rt", "amp"]
for x in range(0, len(content)):
    stringList.append([])
    stringList[x] = content[x].split(" ")

#Used to store the index of the tweet that contains a word in the corpus
idxInCorpus = -1

for x in range(0, len(content)):
    tweetWords = stringList[x]
    numWords = len(tweetWords)
    for i in range (0, numWords):
        word = normalizr.normalize(stringList[x][i].lower())
        stringList[x][i] = word
    for i in range(0, numWords):
        firstWord = stringList[x][i]
        if (x==idxInCorpus or (stringList[x][i] in crpNodeList)):
            idxInCorpus = x
            for j in range(i+1, numWords):
                secondWord = stringList[x][j]
                if graph.has_edge(firstWord, secondWord):
                    updatedWeight = graph[firstWord][secondWord]['weight'] + 1
                    graph.add_edge(firstWord, secondWord, weight=updatedWeight)
                elif corpus.has_edge(firstWord, secondWord):
                    crpEdgeWeight = corpus[firstWord][secondWord]['weight']
                    graph.add_edge(firstWord, secondWord, weight=crpEdgeWeight)
                elif (firstWord not in bannedWords) and (secondWord not in bannedWords):
                    graph.add_edge(firstWord, secondWord, weight=minEdgeWeight)

edgeList = graph.edges()

for edge in edgeList:
    dict = graph.get_edge_data(*edge)
    edgeWeight = dict['weight']
    edgeWeightList.append(edgeWeight)

data = Counter(edgeWeightList)
modes = data.most_common()
print("Modes of edge weight (including their frequency):\r\n" + str(modes))
  
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

print(graph.edges())
        
nx.draw(graph, with_labels = True, node_size=1000, node_color="g", font_size=10)
plotter.show()




