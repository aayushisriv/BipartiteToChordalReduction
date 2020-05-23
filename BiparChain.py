"""
@author- Aayushi Srivastava
The code takes bipartite graph as input, converts it into chain graph then to chordal graph.

"""
import networkx as nx 
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import copy

import operator
import itertools

class BipartCh:

	def __init__(self,noNodes1, noNodes2,noEdges):
		self.noNodes1 = noNodes1
		self.noNodes2 = noNodes2
		self.noEdges = noEdges
		self.W = {}
		self.WEdgeList = []
		self.rankList = []
		self.vertexList1 = []
		self.vertexList2 = []
		self.GEdgeList = []
		self.HEdgeList = []
		self.G = {}
		self.fd = {}
		self.bta = {}
		self.NEdgeList = []
		self.CEdgeList = []
		self.DEdgeList = []
		self.firstrank = []
		self.H = {}
		self.getrank = 0
		self.neb2 = []
		self.rankList1 = []
		self.C2 = {}
		self.C2EdgeList = []
		self.maxv = {}
		self.m_ver1 = 0
		self.maxn = {}
		self.m_ver2 = 0
		self.neb1 = []
		self.neb2 = []



	def createBipartiteGraph(self):
		"""Function to create bipartite graph"""
		self.G = bipartite.gnmk_random_graph(self.noNodes1,self.noNodes2,self.noEdges)

		if type(self.G) is not dict:
			self.G = nx.to_dict_of_lists(self.G)
			print self.G
		for key,value in self.G.iteritems():
			for v in value:
				if key < v:
					e = []
					e.append(key)
					e.append(v)
					self.GEdgeList.append(e)
		self.G = nx.Graph(self.G)
		#self.checkChain(self.G)
		for i in range (0,self.noNodes1):
			self.vertexList1.append(i)
		for j in range(self.noNodes1,(self.noNodes1+self.noNodes2)):
			self.vertexList2.append(j)
			print "M list",self.vertexList2
		self.plotBipartGraph(self.G)
		self.createChainGraph(self.G)


	def createChainGraph(self,bigraph):
		self.HEdgeList = copy.deepcopy(self.GEdgeList)
		self.H = copy.deepcopy(self.G)
		print "---START CONVERTING FROM BIPARTITE GRAPH TO CHAIN GRAPH---"
		self.chaindeck(self.vertexList1,self.vertexList2,self.H)
		self.plotChainGraph(self.G,self.NEdgeList,self.vertexList1,self.vertexList2)
		print "---END CONVERSION FROM BIPARTITE TO CHAIN GRAPH---"
		self.ChordalProcess(self.H)

	def plotBipartGraph(self, graphpl):
		"""plot Bipartite Graph"""
		self.G = nx.Graph(self.G)
		GD = nx.Graph(self.G)
		pos = nx.spring_layout(GD)
		#nx.draw(GD,pos,width=8.0,with_labels=True)
		nx.draw_networkx_nodes(GD,pos, width = 1)
		nx.draw_networkx_edges(GD, pos, width=1.2, alpha=0.5)
		#nx.draw_networkx_edges(GD, pos, edgelist=newEdgeList, width=3.0, alpha=0.5, edge_color='blue')
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		plt.show()


	def chaindeck(self,firstdi,seconddi,graphChain):
		"""Convert Bipartite graph to chain graph based on ranking heuristic"""
		self.H = nx.Graph(self.H)
		print "GList",self.vertexList1
		dv = self.H.degree(self.H)
		print "See Degree list",dv
		dvdict = dict(dv)
		print "Dictinary of node-degree",dvdict
		self.fd =  sorted(dvdict.items(), key=lambda kv:(kv[1],kv[0]))
		print "Sorted node-degree dictionary",self.fd
		for i in self.fd:
			if i[0] in self.vertexList1:
				print "Found",i[0]
				self.firstrank.append((i[0],i[1]))
				print "my new liste", self.firstrank
			elif i[0] not in self.vertexList2:
				print "Not found",i[0]
		rdi = dict(self.firstrank)
		
		self.bta = sorted(rdi.items(), key=lambda kv:(kv[1],kv[0]))
		print "Ranking on index:",self.bta
		print type(self.G)
		for x in self.bta:
			
			ind = self.bta.index(x)
			print "Ranks are below:"
			print "Node---Rank (for first part)"
			print x[0],":",ind
			self.rankList1.append((x[0],ind))
		print "My first side nodes with ranks",self.rankList1
		print "My second vertex list",self.vertexList2
		
		for v2 in self.vertexList2:
			abc = []
			self.neb2 = list(self.H.neighbors(v2))
			if self.neb2:
				print "Neighbors of",v2,"are:",self.neb2
				for y in self.rankList1:
					for j in self.neb2:
						if j == y[0]:
							print "My checks",j,y
							abc.append((y[0],y[1]))
							#print "ABC",abc
							#print "ver",y[0]
							self.getrank = max(abc, key = lambda i:i[1])[1]
							#print type(getrank)
				print type(self.H)
				self.H = nx.Graph(self.H)

				print self.rankList1
				for k in self.rankList1:
					if self.getrank == k[1]:
						print "Hey found Rank of ",v2, k[1]
				for y in self.rankList1:
					if self.getrank > y[1]:
						if self.H.has_edge(v2,y[0]):
							print "Already edge is there between",v2, "and",k[0]
						elif not self.H.has_edge(v2,y[0]):
							self.H.add_edge(v2,y[0])
							self.NEdgeList.append((v2,y[0]))
							print "Edge added between:", v2, "and", y[0]
						elif self.getrank <  y[1]:
							print "Not seen"
					print "New edge list",self.NEdgeList
			if not self.neb2:
				print "No neighbors of the vertex",v2
					
					
		print "New edge list",self.NEdgeList		
		print "Total Edges added to Bipartite Graph to make it Chain graph:",len(self.NEdgeList)
		self.H = nx.to_dict_of_lists(self.H)
		print "Changed",self.H
		self.H = nx.Graph(self.H)
		#vertexlist = vertexlist + vertexList2	
		
		



	def plotChainGraph(self,graphPlot,newEdgeList,vertexList1,vertexList2):
		"""function to plot Chain graph"""
		GD = nx.Graph(self.G)
		pos = nx.spring_layout(GD)
		F = copy.deepcopy(self.G)
		F.add_edges_from(newEdgeList)
		F = nx.to_dict_of_lists(F)
		print "Final chain Graph",F
		#vertexlist = vertexlist + vertexList2
		nx.draw_networkx_nodes(GD, pos, nodelist=(vertexList1 + vertexList2), node_color='red', node_size=300, alpha=0.8)
		#nx.draw_networkx_nodes(GD, pos, nodelist=NEdgeList, node_color='r', node_size=500, alpha=0.8)
			
		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_edges(GD, pos, edgelist=newEdgeList, width=3.0, alpha=0.5, edge_color='blue')
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		#plt.show()
		plt.show()
		#nx.draw(GD,pos,width=8.0,with_labels=True)
		#plt.draw()
		#plt.show()

	def ChordalProcess(self,grapC):
		"""Function to start Chordal graph conversion"""
		self.W = copy.deepcopy(self.H)
		self.WEdgeList = copy.deepcopy(self.HEdgeList)

		print "---START CONVERTING FROM CHAIN GRAPH TO CHORDAL GRAPH"
		#self.ChordalGraph(self.W,self.vertexList1,self.vertexList2)
		
		self.Chordal2(self.C2, self.vertexList1, self.vertexList2)
		self.plotChordalGraph(self.C2,self.CEdgeList,self.DEdgeList,self.vertexList1,self.vertexList2)
		print "---END CONVERSION FROM CHAIN TO CHORDAL GRAPH"
			
	
	def Chordal2(self, graph2, vert1, vert2):
		"""Converted to chordal graph based on the maximum neighborhood vertex and making its neighbors as cliques"""
		self.C2 = copy.deepcopy(self.H)
		self.C2EdgeList = copy.deepcopy(self.HEdgeList)
		print "First one", vert1
		print "Second one", vert2
		#for v in vert1:
		print type(self.H)
		self.H = nx.Graph(self.H)
		dv = list(self.C2.degree(vert1)) #list of tuples
		print "Make deg",dv
		#dv = list(graphtoCons.degree(graphtoCons)) 
		print "see the  degree list:"
		print dv
		#print self.HEdgeList
		dvdict = dict(dv)
		#print "Dictionary of node-degree is", dvdict
		self.maxv = dict(sorted(dvdict.items(), key=lambda kv:(kv[1], kv[0])))
		#print "Sorted dictionary of node-degree:",self.maxv
		self.m_ver1 = max(self.maxv.keys(), key=(lambda k:self.maxv[k]))
		#print type(self.m_ver1)
		print "Vertex of Maximum Degree is:",self.m_ver1
		self.neb1 = list(self.H.neighbors(self.m_ver1))
		print "Neighbors of the chosen vertex are:",self.neb1
		nebcomb1 = list(itertools.combinations(self.neb1,2))
		print "See combinations of first side:",nebcomb1
		for p in nebcomb1:
			print p
			self.C2.add_edges_from(nebcomb1)
			self.CEdgeList.append(p)
		print "My List for vertex1", self.CEdgeList
		print "Edges added in first part of graph to make it chordal",len(self.CEdgeList)
		neblen = len(self.neb1)
		#for n in vert2:
			#print type(self.H)
		self.H = nx.Graph(self.H)
		nv = list(self.C2.degree(vert2)) #list of tuples
		#dv = list(graphtoCons.degree(graphtoCons)) 
		print "see the  degree list:"
		print nv
		#print self.HEdgeList
		nvdict = dict(nv)
		#print "Dictionary of node-degree is", nvdict
		self.maxn = dict(sorted(nvdict.items(), key=lambda kv:(kv[1], kv[0])))
		#print "Sorted dictionary of node-degree:",self.maxn
		self.m_ver2 = max(self.maxn.keys(), key=(lambda k:self.maxn[k]))
		#print type(self.m_ver2)
		print "The chosen vertex of maximum degree", self.m_ver2
		self.neb2 = list(self.H.neighbors(self.m_ver2))
		
		nebcomb2 = list(itertools.combinations(self.neb2,2))
		
		for q in nebcomb2:
			print q
			self.C2.add_edges_from(nebcomb2)
			self.DEdgeList.append(q)
		#print "My List for vertex2",self.DEdgeList
		print "Edges added in second part of graph to make it chordal",len(self.DEdgeList)
		print "Total edges added to chain graph to make it chordal:",(len(self.CEdgeList) + len(self.DEdgeList))




	def plotChordalGraph(self,graphPlot,newEdgeList1,newEdgeList2,vertexList1,vertexList2):
		GD = nx.Graph(self.H)
		pos = nx.spring_layout(GD)
		J = copy.deepcopy(self.H)
		J.add_edges_from(newEdgeList1 + newEdgeList2)
		J = nx.to_dict_of_lists(J)
		print "Final chain Graph",J
		#vertexlist = vertexlist + vertexList2
		nx.draw_networkx_nodes(GD, pos, nodelist=(vertexList1 + vertexList2), node_color='red', node_size=300, alpha=0.8)
		#nx.draw_networkx_nodes(GD, pos, nodelist=NEdgeList, node_color='r', node_size=500, alpha=0.8)
			
		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_edges(GD, pos, edgelist=newEdgeList1, width=3.0, alpha=0.5, edge_color='blue')

		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_edges(GD, pos, edgelist=newEdgeList2, width=3.0, alpha=0.5, edge_color='green')
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		#plt.show()
		plt.show()


		#Recognition
		self.C2 = nx.Graph(self.C2)
		graph = nx.Graph(self.C2)
		if nx.is_chordal(graph):
			print "Graph: IT IS CHORDAL"
		else:
			print "Graph: NO IT IS NOT CHORDAL"



	
	
val1 = int(raw_input("Enter no. of nodes in first part of graph:"))
val2 = int(raw_input("Enter no. of nodes in second part of graph:"))
val3 = int(raw_input("Enter no. of edges:"))
gvert = BipartCh(val1,val2,val3)
gvert.createBipartiteGraph()  



			







