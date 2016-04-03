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
from kivy.uix.popup import Popup
from kivy.uix.label import Label

#import treelib
from treelib import Tree

#This is to make weight[] selection more legible
left = 0
right = 1

#Default values
defaultEdgeThickness = 2
daxis = [3,1]
dscale = 40
defaultNodeSize = 20

dragSpeed = 5

class InfoWidget(Bubble):
	pass

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
	info_box = None

	def __init__(self, i, color=None, **kwargs):
		super(Node,self).__init__(**kwargs)
		self.i = i
		self.pos_x, self.pos_y = self.pos
		self.info_box=Popup(title=self.tag, content=Label(text='hello, place'), size_hint=(None,None), size=(400,400))
		
		self.ids['handle'].bind(on_release=self.interact)
		
		if there_is(color):
			self.color = color
			
	def interact(self, value):
		if self.get_ctrl().touch_button == 'left':
			if self.get_ctrl().double_click:
				print "expand node "+str(self.i)
				self.info_box.open()
			print "select node", self.i
			self.get_ctrl().select(self)
		elif self.get_ctrl().touch_button == 'right':
			if self.selected:
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
		

class Edge(FloatLayout):

	selected = False
	i = None
	info_box = None

	def __init__(self, i, tail=None, head=None, color=None, **kwargs):
		super(Edge, self).__init__(**kwargs)
		
		if there_is(tail):
			self.tail_x, self.tail_y = tail
		if there_is(head):
			self.head_x, self.head_y = head
		if there_is(color):
			self.color = color
		
		self.x_mod = zero_patch(self.head_x, self.tail_x)
		self.y_mod = zero_patch(self.head_y, self.tail_y)
		self.i = i
		self.info_box=Popup(title=self.tag, content=Label(text='hello, place'), size_hint=(None,None), size=(400,400))
		
		self.ids['handle'].bind(on_release=self.interact)
			
	def interact(self, value):
		if self.get_ctrl().touch_button == 'left':
			if self.get_ctrl().double_click:
				print "expand edge "+str(self.i)
				self.info_box.open()
			print "select edge", self.i
			self.get_ctrl().select(self)
		elif self.get_ctrl().touch_button == 'right':
			if self.selected:
				print "display edge options"
			
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
		
	def drawTree(self, pid=None, nid=0, altroot_pos=None):
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
		self.treeVis.add_node(nid, pos, "Node [ "+str(nid)+" ]")
		
		'''
		For the edge id, since this is a tree, each child only has one parent. Thus, we will use the child the
		edge is leading up to as the edge's index, since we know this will always be a unique value for edges.
		'''
		if nid != 0: self.treeVis.add_edge((pid, nid),root_pos,pos, "Edge [ "+str(pid)+" , " +str(nid)+" ]") #only print the edge if it is not a root
		
		print self.graph_leftmost, self.graph_rightmost, self.graph_bottommost
		for cid in t.get_node(nid).fpointer:
			self.drawTree(nid, cid, pos) #call drawTree on children
			
	def generate_tree(self):
		self.drawTree()
		self.graph_width = self.graph_rightmost - self.graph_leftmost
		self.graph_height = -self.graph_bottommost
		
		print self.graph_width
		print self.graph_height
		
		self.treeVis.graph_size = self.graph_width*self.treeVis.scale_index + 2*self.treeVis.node_radius, self.graph_height*self.treeVis.scale_index + 2*self.treeVis.node_radius
		self.treeVis.pos = -self.graph_leftmost*self.treeVis.scale_index + self.treeVis.node_radius, -self.graph_bottommost*self.treeVis.scale_index + self.treeVis.node_radius
		self.treeVis.ids['graph'].bounding_box = self.treeVis.graph_size[0], self.treeVis.graph_size[1]
		print self.treeVis.ids['graph'].bounding_box

class GraphWidget(Scatter):
	grow_scaler = Matrix().scale(1.1,1.1,1)
	shrink_scaler = Matrix().scale(0.9,0.9,1)
	
	def __init__(self, scale_index=None, **kwargs):
		super(GraphWidget,self).__init__(**kwargs)
		
		if there_is(scale_index):
			self.scale_index = scale_index
	
	def zoom_in(self, focus_pos):
		self.apply_transform(self.grow_scaler, anchor=focus_pos)
		print self, self.size
		
	def zoom_out(self, focus_pos):
		self.apply_transform(self.shrink_scaler, anchor=focus_pos)
		print self, self.size
		
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
	
	def add_node(self, i, input_position, input_tag="n-test"):
		print "ADDING NODE", i
		new_node = Node(i, tag=input_tag, pos=input_position, radius=self.node_radius)
		self.node_widgets[i] = new_node
		self.graph_nodes.add_widget(new_node)
	
	def add_edge(self, i, input_tail, input_head, input_tag="e-test"):
		new_edge = Edge(i, tag=input_tag, tail=input_tail, head=input_head)
		self.edge_widgets[i[1]]=new_edge
		self.graph_edges.add_widget(new_edge)
		
	def get_ctrl(self):
		return self.parent.get_ctrl()

class ScreenWidget(Widget):
	def on_touch_down(self,touch):
		self.get_ctrl().touch_button = touch.button
		self.get_ctrl().double_click = touch.is_double_tap
		print "DOUBLE CLICK:", self.get_ctrl().double_click
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
			
		'''
		THIS IS THE RIGHT-CLICK EVENT
		'''
			
		if touch.button == 'right':
		
			'''
			THIS GETS THE POPUP_MENU: the menu is created in the WindowWidget (see below)
			'''
		
			popup_menu = self.get_ctrl().get_window().popup_menu
			
			popup_menu.open() 
			
			'''
			^ I just did this to make sure the popup_menu worked
			'''

			
	def get_ctrl(self):
		return self.parent.get_ctrl()

class Control(Widget):
	touch_button = ""
	double_click = False
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
		print self.parent.visualizer.edge_widgets[i[1]], self.parent.visualizer.edge_widgets[i[1]].i
		return self.parent.visualizer.edge_widgets[i[1]]
	
		
	def select(self,item):
		if self.selection_1 == None:
			item.select()
			self.selection_1 = item.i
			print "[slot 1]", self.selection_1, self.selection_2
		elif self.selection_2 == None:
			item.select()
			self.selection_2 = item.i
			print "[slot 2]", self.selection_1, self.selection_2
		else:
			self.clear_selection()
			item.select()
			self.selection_1 = item.i
			print "<cycle>", self.selection_1, self.selection_2
			
	def clear_selection(self):
		if there_is(self.selection_1):
			print type(self.selection_1)
			if type(self.selection_1) is int:
				print "INTEGER"
				self.get_graph_node(self.selection_1).deselect()
			elif type(self.selection_1) is tuple:
				self.get_graph_edge(self.selection_1).deselect()
				
		if there_is(self.selection_2):
			print type(self.selection_2)
			if type(self.selection_2) is int:
				print "INTEGER"
				self.get_graph_node(self.selection_2).deselect()
			elif type(self.selection_2) is tuple:
				self.get_graph_edge(self.selection_2).deselect()
		
		self.selection_1, self.selection_2 = None, None
		print "clear selection", self.selection_1, self.selection_2
		
	def get_visualizer(self):
		return self.parent.visualizer
		
	def get_window(self):
		return self.parent
	
class WindowWidget(FloatLayout):
	control = None
	visualizer = None
	popup_menu = None
	
	def __init__(self, **kwargs):
		super(WindowWidget,self).__init__(**kwargs)
		
		'''
		THIS IS WHERE THE POPUP WILL FIRST BE DEFINED
		'''
		
		self.popup_menu = Popup(title='Place Holder', content=Label(text='hello, place'), size_hint=(None,None), size=(400,400))	

		'''
		You can then access the popup from any widget by use of the following commands: 
																		"self.get_ctrl().get_window().popup_menu"
		
		exlpanation:
		-----------
		"get_ctrl()" is a command available to all widgets that returns the Control widget.
		
		"get_window()" is a command from Control that returns the current WindowWidget (yes, this widget, right here).
		
		And yeah, from here, as you can tell, you have acces to the popup_menu
		'''
		
		self.control = Control()
		self.add_widget(self.control)
		
	def take_visualizer(self,v):
		self.visualizer = v
		self.add_widget(self.visualizer)
	
	def get_ctrl(self):
		return self.control
			
class GraphVisbak3App(App):
    def build(self):
		
		t = load("BigTGraph.txt")
		td = treeData(t)
		td.generate_tree()
		td.treeVis
		
		parent = WindowWidget()
		parent.take_visualizer(td.treeVis)
		
		return parent

if __name__ == '__main__':
    GraphVisbak3App().run()

	
'''
How the program works:
---------------------

hierarchy:

	WindowWidget:
		
		relevant instance vars
		-------------
			popup_menu:
		
		children
		--------
			Control:
			TreeVisualizer:
				children
				--------
					ScreenWidget: #think of this not as the screen on which stuff is dislayed, more like a 
								  screen in front of a zoo exhibit. Its purpose is to track touch commands 
								  "over" all the rest of the widgets.#
					GraphWidget:
						children
						--------
							graph_nodes(GraphItems): #Node layer#
							graph_edges(GraphItems): #Edge layer#
				
As aforementioned, from just about any widget, the command "get_ctrl()" is available and returns Control.
'''
		