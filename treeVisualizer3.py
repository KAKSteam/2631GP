
# get system tools
import sys

# import kivy tools
#	this is a "root window" application
from kivy.app import App

#	this provides us drawable and interactable widgets
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.core.window import Window

#	this provides us graphical primitives
from kivy.graphics import Color, Ellipse, Line

#import treelib
from treelib import Tree

#import operator
import operator

#import helper methods
from helper import loadTree, there_is

#import custom Widgets
from kivy_extentions3 import CircularButton

#import visualization widgets
from MovingButtons4 import TreeVisualizer, Node, Edge, GraphWidget, GraphItems

#This is to make weight[] selection mo9re legible
left = 0
right = 1

#Default values
defaultEdgeThickness = 2
defaultColor = (.4, .7, 1, 2)
daxis = [3,1]
dscale = 40
defaultNodeSize = 20

#Object holding relevant data for visualizing the tree
class treeData():

	t = None
	offset = []

	def __init__(self, tree):
		global left
		global right

		#Load tree
		self.t = tree
		
		#Weight will be used to keep track of how many nodes there are on each side of
		#A given node. Offset is the offset between a node and its parent.
		weight = [None] * self.t.size()
		self.offset = [0] * self.t.size()
	
		#Itterate by Depth First Search in reverse to move from the leaves up to the root node.
		nodeIds = self.t.expand_tree(0,Tree.DEPTH)
		
		#For each node, calculate its weight, based on its children, and re-arrange its
		#children according to their weight.
		for nid in reversed(list(nodeIds)):
			node = self.t.get_node(nid)
			
			weight[nid] = [0,0]
		
			if not node.is_leaf():
				midPoint = len(node.fpointer)/2
			
				#For every child, determine if it is left or right from the parent by
				#comparing its index to the midPoint
				for idx, cid in enumerate(node.fpointer):
					if idx < midPoint:
						#LEFT OF PARENT
						self.offset[cid] = idx - midPoint - weight[cid][right]
						weight[nid][left] += self.offset[cid]
					
					if idx >= midPoint:
						#RIGHT TO PARENT
						self.offset[cid] = idx - midPoint + 1 - weight[cid][left]
						weight[nid][right] += self.offset[cid]
		


class TreeWidget(FloatLayout):

	treeVis = None
	treeData = None
	axis = 0
	scale = 0
	nodeWidgets = []
	edgeWidgets = []
	
	def __init__(self, trd, a=daxis, s=dscale,**kwargs):
		#inherits the super constructor from its parent class
		super(TreeWidget,self).__init__(**kwargs)
		self.treeVis = TreeVisualizer()
		
		#Set axis and scale
		self.axis = a
		self.scale = s
		
		#Build treeData object
		self.treeData = trd
			
	def drawTree(self, nid=0, altroot_pos=None):
		#Draws a single node and the edge leading up to it (unless is a root), and then
		#calls it's self on its children.
	
		#Global variables
		global left
		global right
	
		#If no value was passed to the optional arguments nid and altroot_pos, 
		#we are starting from the root of the tree.
		root_pos = self.axis if (altroot_pos == None) else altroot_pos
		
		#Function variables for the sake of clarity
		offset = self.treeData.offset
		t = self.treeData.t
		root_x, root_y = root_pos
		
		#Add the offset of the node under consider
		pos = [root_x + offset[nid], root_y]
		
		#If not root, move the node down by the scale value
		if nid != 0: pos[1] -= 1
		
		#paint the node and the edge leading up to it
		with self.canvas:
			print pos
			self.treeVis.add_node(pos)
			print root_pos, pos
			if nid != 0: self.treeVis.add_edge(root_pos,pos) #only print the edge if it is not a root
		for cid in t.get_node(nid).fpointer:
			self.drawTree(cid, pos) #call drawTree on children
			
		#TODO: optimize by changing it to check if the node if a lead instead of a root so to skip
		#more useless processing and make code cleaner.
		
class TreeVisApp(App):
	def build(self):
		
		parent = FloatLayout()
		
		t = loadTree("TGraphFinal.txt")
		td = treeData(t)
		tree = TreeWidget(td,size_hint=(1,1))
		tree.drawTree()
		
		#tree = FloatLayout(pos=(100,200),size=(100,100),size_hint=(None,None))
		#print tree.pos
		#button = CircularButton(pos_hint={'x': 0, 'top': 1},size=(20,20),size_hint=(None,None))
		#node = NodeWidget(None, pos_hint={'center_x': 0.5, 'center_y': 0.5},size=(20,20),size_hint=(None,None))

		#circle = CircleImage()
		
		#pos1 = (100,100)
		#pos2 = (120,300)
		
		#self.tree.node(pos1,defaultColor)
		#self.tree.node(pos2,defaultColor)
		#self.tree.edge(pos1,pos2,defaultColor)

		#parent.add_widget(self.tree)
		#test = TestWidget()
		#tree.add_widget(node)
		#tree.mytest = test
		#print tree.pos
		#parent.add_widget(test)
		return tree.treeVis
	
TreeVisApp().run()
#tp.drawTree()



#NOTES
#For info, use bubble