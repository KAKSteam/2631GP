#!/usr/bin/env python

from pygraph.classes.digraph import digraph
import sys
import treelib
from treelib import Tree
from treelib import Node

def isInt(val):
	try:
		int(val)
		return True
	except ValueError:
		return False

def isFloat(val):
	try:
		float(val)
		return True
	except ValueError:
		return False

def load(path):

	gtype = None
	graph = None
	nodes = []

	#TEMP: LOAD FILE FROM PATH#
	file = open(path,"r",0)
	#TEMP#

	gtype = file.next() 
	#print isInt(gtype) #ASSERT LINE 0 IS AN INTEGER
	gtype = int(gtype)
	#print gtype

	if (gtype == 0):
		graph = Tree()
		nodes = []
		print 'GRAPH TYPE: TREE'

	if (gtype == 1):
		graph = digraph()		
		print 'GRAPH TYPE: EWD'

	#print type(graph)
	for linenum,line in enumerate(file):
		if (linenum == 0): 
			parts = line.split()
			#print parts[0]

			nodeAttrs = parts[1].split(';')
			numNodeAttrs = nodeAttrs.pop(0)
			#print numNodeAttrs
			#print isInt(numNodeAttrs)

			#print numNodeAttrs, nodeAttrs
			continue

		if (linenum == 1):
			for node in line.split():
				tokens = node.split(';')
				index = tokens.pop(0)
				#print index #in final, assert numNodes == index
				#print isInt(index)
				if (isInt(index)):
					index = int(index)
					if (gtype == 0):
						nodes.append(Node(identifier=index,data=tokens))
						if (index == 0):
							#print "ZERO"
							#n = nodes[0]
							#print type(n)
							graph.add_node(nodes[0])
							#graph.show()
							#print graph.get_node(0)
					if (gtype == 1):
						graph.add_node(index, attrs=tokens)
					#print tokens
					continue

		if (linenum == 2):
			if (gtype == 0):
				#print isInt(line) #ASSERT LINE IS A SINGLE INT
				numEdges = int(line)
			if (gtype == 1):
				parts = line.split()
				#print parts[0]

				lineAttrs = parts[1].split(';')
				numLineAttrs = lineAttrs.pop(0)
				#print numLineAttrs
				#print isInt(numLineAttrs)

				#print numLineAttrs, lineAttrs

				continue

		if (linenum > 2):
			#CHECK THAT PARTS ARE INT
			parts = line.split()
			tail = int(parts[0])
			head = int(parts[1])

			if (gtype == 0):
				graph.add_node(nodes[head],tail)

			if (gtype == 1):
				attributes = parts[2].split(';')
				weight = attributes.pop(0)
				#check head and tail are integers

				#check number attributes

				#print (tail,head), weight, attributes
				graph.add_edge((tail,head),weight,attrs=attributes)

	return graph
