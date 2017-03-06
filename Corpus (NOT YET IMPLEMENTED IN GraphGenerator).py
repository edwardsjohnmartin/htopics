import networkx as nx
import matplotlib.pyplot as plotter
from normalizr import Normalizr

graph = nx.Graph()

fileName = "test timeline.txt"
file = open(fileName, 'r')
fileData = file.readline()
fileData = fileData.split(" ")
fileData = [str for str in fileData if str != ""]
edgeWeight = 1

neighborNum = int(input("Min num neighbors for each node (2 or more):\r\n"))

maximumX = len(fileData)

for x in range(0, maximumX):
    firstWord = fileData[x]
    for y in range(1, min(neighborNum+1, (maximumX-x))):
        secondWord = fileData[x+y]
        if graph.has_edge(firstWord, secondWord):
            edgeWeight = graph[firstWord][secondWord]['weight'] + 1
        else:
            edgeWeight = 1
        graph.add_edge(firstWord, secondWord, weight=edgeWeight)

edgeList = graph.edges()
edgeWeightList = []

for edge in edgeList:
    dict = graph.get_edge_data(*edge)
    edgeWeight = dict['weight']
    edgeWeightList.append(edgeWeight)

print(edgeWeightList)

nx.draw(graph, with_labels = True, node_size=1000, node_color="g", font_size=10)
plotter.show()
