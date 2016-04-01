from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.graphics.transformation import Matrix
from kivy.uix.floatlayout import FloatLayout
from helper import zero_patch, there_is, brighten
from loader import load
from kivy.uix.bubble import Bubble
from kivy.uix.button import Button
from kivy.uix.image import Image

#import treelib
from treelib import Tree

#This is to make weight[] selection mo9re legible
left = 0
right = 1

#Default values
defaultEdgeThickness = 2
daxis = [3,1]
dscale = 40
defaultNodeSize = 20

dragSpeed = 5

class CircularButton(Button):
	
	def __init__(self, **kwargs):
		super(CircularButton, self).__init__(**kwargs)
		self.bind(on_press=self.interact)

	def interact(self, value):
		if self.get_ctrl().touch_button == 'left':
			self.background_color = brighten(self.color, 0.5)

	def get_ctrl(self):
		return self.parent.get_ctrl()
		
class Node(FloatLayout):

	selected = False
	i = None

	def __init__(self, i, color=None, **kwargs):
		super(Node,self).__init__(**kwargs)
		self.selected_mask = Image(source="node_selected.png",pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.02, 0.02)) #size hint is the 1/graph_itemssize
		self.i = i
		self.pos_x, self.pos_y = self.pos
		self.ids['handle'].bind(on_release=self.interact)
		
		if there_is(color):
			self.color = color
			
	def interact(self, value):
		if self.get_ctrl().touch_button == 'left':
			print "select node", self.i
			self.get_ctrl().select(self.i)
		elif self.get_ctrl().touch_button == 'right':
			if not self.selected:
				self.selected = True
			print "display node options"
			
	def select(self):
		if not self.selected:
			self.selected = True
			print self.i, "selected"
			#self.add_widget(self.selected_mask)
			self.ids['handle'].color = brighten(self.color, 0.2)
		
	def deselect(self):
		if self.selected:
			self.selected = False
			print self.i, "deselected"
			#self.remove_widget(self.selected_mask)
			self.ids['handle'].color = self.color
			
	def get_ctrl(self):
		return self.parent.get_ctrl()
		
#Object holding relevant data for visualizing the tree
class treeData():

	t = None
	treeVis = None
	axis = [0,0]
	offset = []
	
	node_radius=40
	
	graph_rightmost = 0
	graph_leftmost = 0
	graph_bottommost = 0
	
	graph_width = 0
	graph_height = 0

	def __init__(self, tree):
		global left
		global right

		#Load tree
		self.t = tree
		self.treeVis = TreeVisualizer(num_nodes=self.t.size(), node_radius=self.node_radius, scale_index=50) #tree visualizer is initialized with correct node number
		#TODO: also get correct edge number
		
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
		offset = self.offset
		t = self.t
		root_x, root_y = root_pos
		
		#Add the offset of the node under consideration
		pos = [root_x + offset[nid], root_y]
		
		print pos
		
		if pos[0] < self.graph_leftmost:
			self.graph_leftmost = pos[0]
			
		if pos[0] > self.graph_rightmost:
			self.graph_rightmost = pos[0]
		
		#If not root, move the node down by the scale value
		if nid != 0: pos[1] -= 1
		if pos[1] < self.graph_bottommost: self.graph_bottommost = pos[1]
		
		#paint the node and the edge leading up to it
		self.treeVis.add_node(nid, pos)
		if nid != 0: self.treeVis.add_edge(root_pos,pos) #only print the edge if it is not a root
		print self.graph_leftmost, self.graph_rightmost, self.graph_bottommost
		for cid in t.get_node(nid).fpointer:
			self.drawTree(cid, pos) #call drawTree on children
			
	def generate_tree(self):
		self.drawTree()
		self.graph_width = self.graph_rightmost - self.graph_leftmost
		self.graph_height = -self.graph_bottommost
		
		print self.graph_width
		print self.graph_height
		
		self.treeVis.graph_size = self.graph_width*self.treeVis.scale_index + 2*self.treeVis.node_radius, self.graph_height*self.treeVis.scale_index + 2*self.treeVis.node_radius
		self.treeVis.pos = -self.graph_leftmost*self.treeVis.scale_index + self.treeVis.node_radius, -self.graph_bottommost*self.treeVis.scale_index + self.treeVis.node_radius
		self.treeVis.ids['graph'].dimensions = self.treeVis.graph_size[0], self.treeVis.graph_size[1]
		print self.treeVis.ids['graph'].dimensions
		
class PopUp(Bubble):
	pass

class GraphWidget(Scatter):
	grow_scaler = Matrix().scale(1.1,1.1,1)
	shrink_scaler = Matrix().scale(0.9,0.9,1)
	
	def __init__(self, scale_index=None, **kwargs):
		super(GraphWidget,self).__init__(**kwargs)
		
		if there_is(scale_index):
			self.scale_index = scale_index
	
	def zoom_in(self, focus_pos):
		self.apply_transform(self.grow_scaler, anchor=focus_pos)
		
	def zoom_out(self, focus_pos):
		self.apply_transform(self.shrink_scaler, anchor=focus_pos)
		
	def move(self, transform_vector):
		delta_x, delta_y = transform_vector
		self.center_x += delta_x
		self.center_y += delta_y
		
	def get_ctrl(self):
		return self.parent.get_ctrl()
	
class GraphItems(FloatLayout):

	def __init__(self, scale_index=None, **kwargs):
		super(GraphItems,self).__init__(**kwargs)
		
		if there_is(scale_index):
			self.scale_index = scale_index
			
	def get_ctrl(self):
		return self.parent.get_ctrl()

class Edge(FloatLayout):
	def __init__(self, tail=None, head=None, color=None, **kwargs):
		super(Edge, self).__init__(**kwargs)
		
		if there_is(tail):
			self.tail_x, self.tail_y = tail
		if there_is(head):
			self.head_x, self.head_y = head
		if there_is(color):
			self.color = color
		
		self.x_mod = zero_patch(self.head_x, self.tail_x)
		self.y_mod = zero_patch(self.head_y, self.tail_y)
		
	def get_ctrl(self):
		return self.parent.get_ctrl()
		
class TreeVisualizer(Widget):
	graph = None
	graph_edges = None
	graph_nodes = None
	screen = None
	
	node_widgets = []
	edge_widgets = []
	
	def __init__(self, num_nodes=128, num_edges=128, node_radius=40, **kwargs):
		super(TreeVisualizer, self).__init__(**kwargs)
		
		self.node_radius = node_radius
		
		#Node widget list and edge list are initialized with a given size so to allow us to insert items
		#using their id as an index
		self.node_widgets=[None]*num_nodes
		self.edge_widgets=[None]*num_edges
		
		self.graph = self.ids['graph']
		self.graph_edges = self.ids['graph_edges']
		self.graph_nodes = self.ids['graph_nodes']
		self.screen = self.ids['screen']
	
	def add_node(self, i, input_position):
		new_node = Node(i, pos=input_position, radius=self.node_radius)
		self.node_widgets[i] = new_node
		self.graph_nodes.add_widget(new_node)
	
	def add_edge(self, input_tail, input_head):			#TODO: update to input using indices (coz at the moment its bassically a huge list of nones with the edges appended to the end)
		new_edge = Edge(tail=input_tail, head=input_head)
		self.edge_widgets.append(new_edge)
		self.graph_edges.add_widget(new_edge)
		
	def get_ctrl(self):
		return self.parent.get_ctrl()

class ScreenWidget(Widget):
	def on_touch_down(self,touch):
		self.get_ctrl().touch_button = touch.button
		if touch.button == 'middle':
			touch.grab(self)
		elif touch.button == 'scrollup':
			self.parent.graph.zoom_in(touch.pos)
		elif touch.button == 'scrolldown':
			self.parent.graph.zoom_out(touch.pos)
		elif touch.button == 'left':
			if not self.get_ctrl().ctrl_down:
				self.get_ctrl().clear_selection()
			
	def on_touch_move(self, touch):
		if touch.grab_current is self:
			x, y = touch.pos
			x0, y0 = touch.ppos
			transform_vector = (x-x0, y-y0)
			self.parent.graph.move(transform_vector)
			
	def on_touch_up(self, touch):
		if touch.grab_current is self:
			touch.ungrab(self)
			
	def get_ctrl(self):
		return self.parent.get_ctrl()

class Control(Widget):
	touch_button = ""
	selection_1, selection_2 = None, None
	
	graph_tools = []
	
	node_tools = []
	edge_tools = []
	
	ctrl_down = False
	
	def __init__(self, **kwargs):
		super(Control,self).__init__(**kwargs)
		
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
		self._keyboard.bind(on_key_up=self._on_keyboard_up)
		
	#IO TOOLS
	#Load/save etc functions to come
		
	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None
		
	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		if keycode[1] == 'lctrl':
			if self.ctrl_down == False:
				self.ctrl_down = True
		if keycode[1] == 'd':
			print self.selection_1, self.selection_2
		return True
		
	def _on_keyboard_up(self, keyboard, keycode):
		if keycode[1] == 'lctrl':
			self.ctrl_down = False
		return True
	
	#GRAPH MANAGEMENT
	def get_graph_node(self,i):
		print self.parent.visualizer.node_widgets[i], self.parent.visualizer.node_widgets[i].i
		return self.parent.visualizer.node_widgets[i]
		
	def get_graph_edge(self,i):
		return self.parent.visualizer.edge_widgets[i]
		
	def select(self,i):		#yet to implement this for edges
		if self.selection_1 == None:		#NOTE: clear other selection if would result in selecting an edge and a node???
			self.get_graph_node(i).select()
			self.selection_1 = i
			print "[slot 1]", self.selection_1, self.selection_2
		elif self.selection_2 == None:
			self.get_graph_node(i).select()
			self.selection_2 = i
			print "[slot 2]", self.selection_1, self.selection_2
		else:
			self.clear_selection()
			self.get_graph_node(i).select()
			self.selection_1 = i
			print "<cycle>", self.selection_1, self.selection_2
			
	def clear_selection(self):
		if there_is(self.selection_1):
			self.get_graph_node(self.selection_1).deselect()
		if there_is(self.selection_2):
			self.get_graph_node(self.selection_2).deselect()
		self.selection_1, self.selection_2 = None, None
		print "clear selection", self.selection_1, self.selection_2
		
	
class WindowWidget(FloatLayout):
	control = None
	visualizer = None
	
	def __init__(self, **kwargs):
		super(WindowWidget,self).__init__(**kwargs)
		self.control = Control()
		self.add_widget(self.control)
		
	def take_visualizer(self,v):
		self.visualizer = v
		self.add_widget(self.visualizer)
	
	def get_ctrl(self):
		return self.control
			
class TreeVisApp(App):
    def build(self):
		
		t = load("BigTGraph.txt")
		td = treeData(t)
		td.generate_tree()
		td.treeVis
		
		parent = WindowWidget()
		parent.take_visualizer(td.treeVis)
		'''
		treevis = TreeVisualizer()
		treevis.add_edge((0,2),(4,4))
		treevis.add_edge((4,4),(6,2))
		treevis.add_node((0,2))
		treevis.add_node((4,4))
		treevis.add_node((6,2))
		parent.add_widget(treevis)
		'''
		
		return parent

if __name__ == '__main__':
    TreeVisApp().run()
'''
Notes
Nice colors: 
	1,0.4,0.5,1
'''

#ALSO: fix the graph widget so it is no longer scatter??? so to fix maybe this ^ thing by not
#having to care about box size anymore, also to fix the button scalling issue
#Finish implementing thing for edge index so select works for both nodes and edges
#Make highlight() functions for edges and nodes and test and link them to select() functions
#connect nodes and edges to their data representations and put the data rep of the tree somewhere too
#Single paramater for graph scale (coz right now you have one for each graph_item planes (edge/node)