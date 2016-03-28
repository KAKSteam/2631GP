
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

#This is to make weight[] selection mo9re legible
left = 0
right = 1

#Default values
defaultEdgeThickness = 2
defaultColor = (.4, .7, 1, 2)
daxis = [320,300]
dscale = 40
defaultNodeSize = 20

#class GraphWidget(FloatLayout):
class NodeWidget(FloatLayout):
	
		#Instance variables
		color = defaultColor
		tag = ""
		data = None
		handle = None
	
		#Initializer
		def __init__(self, data_in, input_color=None, input_tag=None, input_data=None, **kwargs):
			super(NodeWidget,self).__init__(**kwargs)
			
			self.data = data_in
			if there_is(input_color):
				self.color = input_color
			if there_is(input_tag):
				self.label = input_tag
			if there_is(input_data):
				self.data = input_data
			self.handle = Button(pos_hint={'x': 0, 'y': 0}, background_color=self.color)
			self.add_widget(self.handle)
			self.handle.bind(on_press=self.hey)
			
		#def update(self):
			#self.clear()
		
		def hey(self,play_btn):
			self.handle.x = self.handle.x + 1
			#self.handle.canvas.ask_update()
			print self.handle.pos

class EdgeWidget(Widget):

		#Instance variables
		tail_pos = [0,0]
		head_pos = [0,0]
		label = ""
		data = None
		handle = None
		
		

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
		


class TreeWidget(Widget):

	treeData = None
	axis = 0
	scale = 0
	nodeWidgets = []
	edgeWidgets = []
	mytest = None
	
	def on_touch_down(self, touch):
			print "hey"
	
	def __init__(self, trd, a=daxis, s=dscale,**kwargs):
		#inherits the super constructor from its parent class
		super(TreeWidget,self).__init__(**kwargs)
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
		
		#Set axis and scale
		self.axis = a
		self.scale = s
		
		#Build treeData object
		self.treeData = trd

	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None
		
	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		if keycode[1] == 'w':
			print "w"
		return True
		
	#This function draws a node in the widget (todo: change Nodes to be of Widget class and add to this widget)
	def node(self, pos, col=defaultColor):
		x, y = pos
		color = (1,0,0,1)

		with self.canvas:
			Color(*color)
			r = defaultNodeSize
			Ellipse(pos=(x - r / 2, y - r / 2), size=(r, r))
		
	#This function draws an edge in the widget (todo: change Edges to be of Widget class and add to this widget)
	def edge(self, pos1, pos2, col = defaultColor, edgeThickness = defaultEdgeThickness):
		x1, y1 = pos1
		x2, y2 = pos2
		color = col

		with self.canvas:
			Color(*color)
			d = defaultNodeSize
			Line(points=[x1,y1,x2,y2], width = edgeThickness)
			
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
		pos = [root_x + offset[nid]*self.scale, root_y]
		
		#If not root, move the node down by the scale value
		if nid != 0: pos[1] -= 1*self.scale
		
		#paint the node and the edge leading up to it
		with self.canvas:
			self.node(pos)
			if nid != 0: self.edge(root_pos,pos) #only print the edge if it is not a root
		for cid in t.get_node(nid).fpointer:
			self.drawTree(cid, pos) #call drawTree on children
			
		#TODO: optimize by changing it to check if the node if a lead instead of a root so to skip
		#more useless processing and make code cleaner.
		
class TestWidget(Widget):
	def on_touch_down(self, touch):
			if touch.button == 'right':
				print "hey"
	def thing(self):
		print "thing"
		
class MainApp(App):
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
		parent.add_widget(tree)
		#tree.mytest = test
		#print tree.pos
		#parent.add_widget(test)
		return parent

	def clearCanvas(self, obj):
		self.painter.canvas.clear()
		print 'Clearing canvas!'
	
MainApp().run()
#tp.drawTree()



#NOTES
#For info, use bubble