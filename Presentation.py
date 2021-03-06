import sys
import nltk
import networkx as nx
import matplotlib.pyplot as plotter
from normalizr import Normalizr
from collections import Counter

normalizr = Normalizr(language='en')

#Corpus variables
#corpus = nx.Graph()
#crpFileName = "us history timeline v2.txt"
#crpFileName = "history.txt"
#crpFile = open(crpFileName, 'r')
#crpLines = crpFile.readline()
#crpLines = crpLines.split(" ")
#crpLines = [str for str in crpLines if str != ""]

#crpLines = set()#[]
#with open(crpFileName,'r') as f:
    #for line in f:
        #for word in line.split():
            #if (word != "" and len(word) > 2 and word[0].isupper() and word[1].islower()):
            #crpLines.append(word)
            #crpLines.add(word)

#crpEdgeWeight = 1
#capNodeWeight = 5
#crpMaxX = len(crpLines)

#neighborNum = int(input("Min num neighbors for each node (2 or more):\r\n"))

#Graph variables
graph = nx.Graph()
#fileName = "a.txt"
fileName = "user tweets.txt"
if (len(sys.argv) > 1):
    fileName = sys.argv[1]
historyData = set()
historyFile = open("a.txt", 'r')
historyData = historyFile.readlines()
readFile = open(fileName, 'r')
stringList = []
content = readFile.readlines()
numWords = 0
minEdgeWeight = 1
edgeWeightList = []
#print(len(content))

'''
#Creates the corpus----------------------------------------------------
words = [normalizr.normalize(word) for word in crpLines]
words = [word for word in words if len(word) > 1]
words = [word.lower() for word in words]
tagged = nltk.tag.pos_tag(words)
#print(crpLines[0])
propernouns = [word for word,pos in tagged if pos == 'NNP' or pos == 'NP']
print("words " + str(len(words)))
print("lines " + str(len(crpLines)))
print("proper nouns = " + str(len(propernouns)))
with open('names.txt', 'w') as f:
    for n in propernouns:
        f.write("%s " % n)
#print(len(words))
#print(len(propernouns))
numWords = len(propernouns)
#for x in range(0, crpMaxX):  
for x in range(0, numWords):  
    if (x % 100 == 0):
        print(x)
    #for y in range(1, min(neighborNum+1, (crpMaxX-x))):
    for y in range(1, min(neighborNum+1, (numWords-x))):
        #firstWord = crpLines[x]
        #secondWord = crpLines[x+y]
        firstWord = propernouns[x]
        secondWord = propernouns[x+y]
        if (True):#firstWord[0].isupper() and firstWord[1].islower() and secondWord[0].isupper() and secondWord[1].islower()):
            firstWord = firstWord.lower()
            secondWord = secondWord.lower()
            w = crpEdgeWeight
            if corpus.has_edge(firstWord, secondWord):
                dict = corpus.get_edge_data(firstWord, secondWord)
                w = dict['weight']
                corpus.add_edge(firstWord, secondWord, weight=w+crpEdgeWeight)
            else:
                corpus.add_edge(firstWord, secondWord, weight=crpEdgeWeight)
            
        #if (firstWord != secondWord):
        #    crpEdgeWeight = 1
        #    if (firstWord[0].isupper()):
        #        crpEdgeWeight = crpEdgeWeight + capNodeWeight
        #    if (secondWord[0].isupper()):
        #        crpEdgeWeight = crpEdgeWeight + capNodeWeight
        #        
        #    firstWord = firstWord.lower()
        #    secondWord = secondWord.lower()
        #        
        #    if corpus.has_edge(firstWord, secondWord):
        #        dict = corpus.get_edge_data(firstWord, secondWord)
        #        crpEdgeWeight = dict['weight']
        #        crpEdgeWeight = crpEdgeWeight * 2
        #    else:
        #        corpus.add_edge(firstWord, secondWord, weight=crpEdgeWeight)

crpEdgeList = corpus.edges()
crpEdgeWeightList = []
crpNodeList = corpus.nodes()

#for edge in crpEdgeList:
#    dict = corpus.get_edge_data(*edge)
#    edgeWeight = dict['weight']
#    edgeWeightList.append(edgeWeight)

#nx.draw(corpus, with_labels = True, node_size=1000, node_color="g", font_size=10)
#plotter.show()

#exit()

#--------------------------------------------------------------------
'''

bannedWords = ["", "rt", "amp"]
for x in range(0, len(content)):
    stringList.append([])
    stringList[x] = content[x].split(" ")

#Used to store the index of the tweet that contains a word in the corpus
dxInCorpus = -1

for x in range(0, len(content)):
    if (x % 100 == 0):
        print("tweet " + str(x) + " of " + str(len(content)))
    tweetWords = stringList[x]
    numWords = len(tweetWords)
    for i in range (0, numWords):
        word = normalizr.normalize(stringList[x][i].lower())
        stringList[x][i] = word
    #numWordsInCorpus = 0;
    for i in range(0, numWords):
        word = stringList[x][i]
        #if (word in crpNodeList):
         #   numWordsInCorpus = numWordsInCorpus + 1;
    #if (numWordsInCorpus > 1):
        for i in range(0, numWords):
            firstWord = stringList[x][i]
            for j in range(i+1, numWords):
                secondWord = stringList[x][j]
                w = 1
                #if (firstWord in crpNodeList or secondWord in crpNodeList):
                #if (firstWord in crpNodeList and secondWord in crpNodeList):
                if graph.has_edge(firstWord, secondWord):
                    updatedWeight = graph[firstWord][secondWord]['weight'] + w
                    graph.add_edge(firstWord, secondWord, weight=updatedWeight)
                        #elif corpus.has_edge(firstWord, secondWord):
                        #    crpEdgeWeight = corpus[firstWord][secondWord]['weight']
                        #    graph.add_edge(firstWord, secondWord, weight=crpEdgeWeight)
                elif (firstWord not in bannedWords) and (secondWord not in bannedWords):
                    #graph.add_edge(firstWord, secondWord, weight=minEdgeWeight)
                    graph.add_edge(firstWord, secondWord, weight=w)
                    
edgeList = graph.edges()

#print("edges = ", graph.edges())

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
        
#nx.draw(corpus, with_labels = True, node_size=1000, node_color="g", font_size=10)
nx.draw(graph, with_labels = True, node_size=1000, node_color="g", font_size=10)
plotter.show()

