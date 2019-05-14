# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 22:55:54 2019

@author: Kiooola
"""


class Node(object):
    def __init__(self,name):
        self.name = name
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    
class Edge(object):
    def __init__(self,src,dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return self.src.getName() + '->' + self.dest.getName()
    
class Diagraph(object):
    
    def __init__(self):
        self.edges = {}
        
    def addNode(self,node):
        if node in self.edges:
            raise ValueError("Duplicate Node")
        else:
            self.edges[node] = []
            
    def addEdge(self,edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not (src in self.edges and dest in self.edges):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
            
    def childrenOf(self,node):
        return self.edges[node]
    
    def hasNode(self,node):
        return node in self.edges
    
    def getNode(self,name):
        for node in self.edges:
            if node.getName() == name:
                return node
            
    def __str__(self):
        result = ''
        for src in self.edges:
            for dest in self.edges[src]:
                result = result + src.getName() + '->'\
                         + dest.getName() + '\n'
        return result[:-1] #omit final newline
                
class Graph(Diagraph):
    def addEdge(self,edge):
        Diagraph.addEdge(self,edge)
        rev = Edge(edge.getDestination(),edge.getSource())
        Diagraph.addEdge(self,rev)
    
def buildCityGraph(graphType):
    g = graphType()
    for name in ('Boston', 'Providence', 'New York', 'Chicago',
                 'Denver', 'Phoenix', 'Los Angeles'): #Create 7 nodes
        g.addNode(Node(name))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('Providence')))
    g.addEdge(Edge(g.getNode('Boston'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('Boston')))
    g.addEdge(Edge(g.getNode('Providence'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('New York'), g.getNode('Chicago')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Denver')))
    g.addEdge(Edge(g.getNode('Chicago'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('Phoenix')))
    g.addEdge(Edge(g.getNode('Denver'), g.getNode('New York')))
    g.addEdge(Edge(g.getNode('Los Angeles'), g.getNode('Boston')))
    return g 

def printPath(path):
    """Assumes path is a list of nodes"""
    result = ""
    for i in path:
        result = result + i.getName()+"->"
    print(result[:-2])
  
    

def dfs (graph, start, end, shortest=None, path=[]):
    
    path = path + [start]
    print('Current DFS path:', printPath(path))
    
    if start==end:
        return path
    
    for node in graph.childrenOf(start):
        if node not in path:
            if shortest == None or len(path) < len(shortest):
                new_path = dfs(graph, node, end, shortest, path)
                if new_path:
                    shortest = new_path
    return shortest


def dfss(graph,start,end):
    print('dfss')
    initPath = [start]
    pathStack = [initPath]
    shortest = None
    
    while len(pathStack)>0:
        current = pathStack.pop()
        if current[-1] == end:
            if shortest == None or len(current)<len(shortest):
                shortest = current
                continue
        
        for node in graph.childrenOf(current[-1]):
            if node not in current:
                new = current + [node]
                pathStack.append(new)
                
    return shortest
        
def bfs(graph, start, end):
    initPath = [start]
    pathQ = [initPath]
    
    while len(pathQ)>0:
        current = pathQ.pop(0)
        if current[-1] == end:
            return current
        for node in graph.childrenOf(current[-1]):
            if node not in current:
                new = current + [node]
                pathQ.append(new)    
        

city_flights = buildCityGraph(Diagraph) 
x = bfs(city_flights,city_flights.getNode('Boston'),city_flights.getNode('Phoenix'))
print("----------")
printPath(x)



                



