#!/usr/bin/env python3

import re
import itertools

ROLLNUM_REGEX = "201[0-9]{4}"

class Graph(object):
	name = "Rahul Kukreja"
	email = "rahul18254@iiitd.ac.in"
	roll_num = "2018254"

	def __init__ (self, vertices, edges):
		"""
		Initializes object for the class Graph

		Args:
			vertices: List of integers specifying vertices in graph
			edges: List of 2-tuples specifying edges in graph
		"""

		self.vertices = vertices
		
		ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
		
		self.edges    = ordered_edges
		
		self.validate()

	def validate(self):
		"""
		Validates if Graph if valid or not

		Raises:
			Exception if:
				- Name is empty or not a string
				- Email is empty or not a string
				- Roll Number is not in correct format
				- vertices contains duplicates
				- edges contain duplicates
				- any endpoint of an edge is not in vertices
		"""

		if (not isinstance(self.name, str)) or self.name == "":
			raise Exception("Name can't be empty")

		if (not isinstance(self.email, str)) or self.email == "":
			raise Exception("Email can't be empty")

		if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
			raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

		if not all([isinstance(node, int) for node in self.vertices]):
			raise Exception("All vertices should be integers")

		elif len(self.vertices) != len(set(self.vertices)):
			duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

			raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

		edge_vertices = list(set(itertools.chain(*self.edges)))

		if not all([node in self.vertices for node in edge_vertices]):
			raise Exception("All endpoints of edges must belong in vertices")

		if len(self.edges) != len(set(self.edges)):
			duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

			raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))

	def min_dist(self, start_node, end_node):
		"""
		Finds minimum distance between start_node and end_node

		Args:
			start_node: Vertex to find distance from
			end_node: Vertex to find distance to

		Returns:
			An integer denoting minimum distance between start_node
			and end_node
		"""
		c=0
		q=[start_node]
		l=[]
		for i in range(len(self.vertices)):
			if self.vertices[i]!=start_node: 
				l.append([])
				l[i].append(self.vertices[i])
				l[i].append(None)
			else:
				l.append([])
				l[i].append(self.vertices[i])
				l[i].append(0)
		source=start_node
		while len(q)!=0:
			for k in range(len(l)):
				if l[k][0]==source:
					temp=k
			for i in range(len(self.edges)):
				if source==self.edges[i][0]:
					for j in range(len(l)):
		   				if l[j][0]==self.edges[i][1] and l[j][1]==None:
		   					l[j][1]=l[temp][1]+1
		   					q.append(self.edges[i][1]) 
				elif source==self.edges[i][1]:
		  			for j in range(len(l)):
		  				if l[j][0]==self.edges[i][0] and l[j][1]==None:
		  					l[j][1]=l[temp][1]+1
		  					q.append(self.edges[i][0])
			q.pop(0)
			if len(q)!=0:
				source=q[0] 
		for i in range(len(l)):
			if l[i][0]==end_node:
				dist=l[i][1]
	
		return dist
		raise NotImplementedError


	def all_paths(self, start_node, end_node, dist, path, path_final):
		"""
		Finds all paths from node to destination with length = dist

		Args:
			node: Node to find path from
			destination: Node to reach
			dist: Allowed distance of path
			path: path already traversed

		Returns:
			List of path, where each path is list ending on destination

			Returns None if there no paths
		"""
		path=path+[start_node]
		if len(path)==dist+1:	
			if start_node==end_node:
				return path
			else:
				return None
		for i in range(len(self.edges)):
			if start_node==self.edges[i][0] and self.edges[i][1] not in path:
				path_final.append(self.all_paths(self.edges[i][1],end_node,dist,path,path_final))	
			elif start_node==self.edges[i][1] and self.edges[i][0] not in path:
				path_final.append(self.all_paths(self.edges[i][0],end_node,dist,path,path_final))
	
		return path_final

		raise NotImplementedError

	def all_shortest_paths(self, start_node, end_node, dist, path, path_final, shortest_paths):
		"""
		Finds all shortest paths between start_node and end_node

		Args:
			start_node: Starting node for paths
			end_node: Destination node for paths

		Returns:
			A list of path, where each path is a list of integers.
		"""
		self.all_paths(start_node,end_node,dist,path,path_final)
		for i in range(len(path_final)):
			if path_final[i]!=None and isinstance(path_final[i][0],int):
				shortest_paths.append(path_final[i])

		return shortest_paths

		raise NotImplementedError

	def betweenness_centrality(self, node):
		"""
		Find betweenness centrality of the given node

		Args:
			node: Node to find betweenness centrality of.

		Returns:
			Single floating point number, denoting betweenness centrality
			of the given node
		"""
		betweenness_centrality=0
		for i in range(len(self.vertices)):
			if self.vertices[i]!=node:
				for j in range(i+1,len(self.vertices)):
					if self.vertices[j]!=node:
						dist=self.min_dist(self.vertices[i],self.vertices[j])
						if dist!=None:
							y=0
							shortest_paths=[]
							self.all_shortest_paths(self.vertices[i], self.vertices[j], dist, [], [], shortest_paths)
							x=len(shortest_paths)
							for k in range(len(shortest_paths)):
								if node in shortest_paths[k]:
									y=y+1
							betweenness_centrality=betweenness_centrality+(y/x)
						
		return betweenness_centrality

		raise NotImplementedError

	def standardized_betweenness_centrality(self,node):
		'''Calculates the standardized betweenness centrality of any given node'''

		n=len(self.vertices)
		standardized_betweenness_centrality=(self.betweenness_centrality(node))/(((n-1)*(n-2))/2)
	
		return standardized_betweenness_centrality

	def top_k_betweenness_centrality(self):
		"""
		Find top k nodes based on highest equal betweenness centrality.

		
		Returns:
			List a integer, denoting top k nodes based on betweenness
			centrality.
		"""
		top_k=[]
		l=[]
		c=0
		for i in range(len(self.vertices)):
			l.append([])
			l[i].append(self.vertices[i])
			l[i].append(self.standardized_betweenness_centrality(self.vertices[i]))	
		l.sort(key = lambda x: x[1], reverse=True)
		k=l[0][1]
		for i in range(len(l)):
			if l[i][1]==k:
				c=c+1 
		top_k=l[:c]

		return top_k
		raise NotImplementedError

if __name__ == "__main__":
	vertices = [1, 2, 3, 4, 5, 6]
	edges    = [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5), (4, 6), (3, 6)]
	#vertices = [0, 1, 2, 3, 4, 5, 6, 7]
	#edges=[(3,6),(3,2),(2,5),(2,4),(5,6),(5,1),(1,0),(4,1)]

	graph = Graph(vertices, edges)

print(graph.top_k_betweenness_centrality())

