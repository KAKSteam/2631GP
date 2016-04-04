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
zoom_speed = 17
#drag_speed = 1

scale_treshold = 45

zoom_out_limit = 0
zoom_in_limit = 1500

class TagWidget(FloatLayout):
	def __init__(self, **kwargs):
		super(TagWidget, self).__init__(**kwargs)

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
	data = []
	
	tag_widget = None
	info_box = None
	info_text = ""
	
	tag_index=0

	def __init__(self, i, data=None, color=None, **kwargs):
		super(Node,self).__init__(**kwargs)
		self.i = i
		self.pos_x, self.pos_y = self.pos
		
		self.ids['handle'].bind(on_release=self.interact)
		
		if there_is(color):
			self.color = color
		if there_is(data):
			self.data = data
		
		self.tag = self.data[self.tag_index] if (len(self.data)>0) else "node "+str(self.i)
		self.info_box=Popup(title=self.tag, content=Label(text='<data void>'), size_hint=(None,None), size=(400,400))
		
		#Size correcting in case the tag is of length 128
	
	def generate_tag(self):
		print "NODE TAG", self.tag
		self.tag_widget = TagWidget(target_x=self.x,target_y=self.y,target_radius=self.radius,tag=self.tag)
		self.tag_widget = TagWidget(target_x=self.x,target_y=self.y,target_radius=self.radius,tag=self.tag)
	
	def show_tag(self):
		self.parent.add_widget(self.tag_widget)
	
	def hide_tag(self):
		self.parent.remove_widget(self.tag_widget)
		
	def generate_info_text(self):
		attrs = self.get_ctrl().graph_data.nodeAttrs
		if len(attrs) <= 0: return
		for attr, val in zip(attrs, self.data):
			self.info_text += str(attr) + ": " + str(val) + "\n"
		self.info_box.content.text = self.info_text
		
	def rotate_tag(self):
		if len(self.data) <= 0: return
		new_index = (self.tag_index + 1)%len(self.data)
		self.change_tag(new_index)
		
	def change_tag(self, idx):
		if idx < 0 or idx >= len(self.data):
			print "idx out of range; the tag was not changed"
			return
		self.tag_index = idx
		
		self.refresh_tag_data()
	
	def refresh_tag_data(self):
		self.tag = self.data[self.tag_index]
		self.tag_widget.tag = self.tag
		self.info_box.title = self.tag
		
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
	data = []
	
	tag_widget = None
	info_box = None
	info_text = ""
	
	tag_index=0

	def __init__(self, i, tail=None, head=None, data=None, color=None, **kwargs):
		super(Edge, self).__init__(**kwargs)
		
		if there_is(tail):
			self.tail_x, self.tail_y = tail
		if there_is(head):
			self.head_x, self.head_y = head
		if there_is(color):
			self.color = color
		if there_is(data):
			self.data = data
		
		self.x_mod = zero_patch(self.head_x, self.tail_x)
		self.y_mod = zero_patch(self.head_y, self.tail_y)
		self.i = i
		
		self.tag = self.data[self.tag_index] if (len(self.data)>0) else "edge "+str(self.i)
		self.info_box=Popup(title=self.tag, content=Label(text='<data void>'), size_hint=(None,None), size=(400,400))
		
		self.ids['handle'].bind(on_release=self.interact)
	
	def generate_tag(self):
		print self.tag
		print self.i, self.tail_x, self.tail_y, self.head_x, self.head_y
		handle_x, handle_y = (self.head_x + self.tail_x)*0.5, (self.head_y + self.tail_y)*0.5
		print handle_x, handle_y
		self.tag_widget = TagWidget(target_x=handle_x,target_y=handle_y,target_radius=self.handle_size,tag=self.tag)
		self.tag_widget = TagWidget(target_x=handle_x,target_y=handle_y,target_radius=self.handle_size,tag=self.tag)
		
	def show_tag(self):
		self.parent.add_widget(self.tag_widget)
	
	def hide_tag(self):
		self.parent.remove_widget(self.tag_widget)
		
	def generate_info_text(self):
		attrs = self.get_ctrl().graph_data.edgeAttrs
		if len(attrs) <= 0: return
		for attr, val in zip(attrs, self.data):
			self.info_text += str(attr) + ": " + str(val) + "\n"
		self.info_box.content.text = self.info_text
		
	def rotate_tag(self):
		if len(self.data) <= 0: return
		new_index = (self.tag_index + 1)%len(self.data)
		self.change_tag(new_index)
		
	def change_tag(self, idx):
		if idx < 0 or idx >= len(self.data):
			print "idx out of range; the tag was not changed"
			return
		self.tag_index = idx
		
		self.refresh_tag_data()
	
	def refresh_tag_data(self):
		self.tag = self.data[self.tag_index]
		self.tag_widget.tag = self.tag
		self.info_box.title = self.tag
	
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
		
	#final variable determining how much space we want around the graph and screen edge
	#when it is first drawn
	border = 100

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
		
	def build_items(self, pid=None, nid=0, altroot_pos=None):
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
		#Get node
		node = t.get_node(nid)
		input_data = node.data
		
		print pos
		
		if pos[0] < self.graph_leftmost:
			self.graph_leftmost = pos[0]
			
		if pos[0] > self.graph_rightmost:
			self.graph_rightmost = pos[0]
		
		#If not root, move the node down by the scale value
		if nid != 0: pos[1] -= 1
		if pos[1] < self.graph_bottommost: self.graph_bottommost = pos[1]
		
		#paint the node and the edge leading up to it
		self.treeVis.add_node(nid, pos,input_data)
		
		'''
		For the edge id, since this is a tree, each child only has one parent. Thus, we will use the child the
		edge is leading up to as the edge's index, since we know this will always be a unique value for edges.
		'''
		
		#t.edgeAttrs = ["element","time","animal"]
		
		if nid != 0: self.treeVis.add_edge((pid, nid),root_pos,pos) #only print the edge if it is not a root
		
		print self.graph_leftmost, self.graph_rightmost, self.graph_bottommost
		for cid in t.get_node(nid).fpointer:
			self.build_items(nid, cid, pos) #call build_items on children
			
	def load_tree(self):
		self.build_items()
		self.treeVis.generate_tree()
		self.graph_width = self.graph_rightmost - self.graph_leftmost
		self.graph_height = -self.graph_bottommost
		
		print self.graph_width
		print self.graph_height
		
		self.treeVis.graph_width = self.graph_width
		self.treeVis.graph_height = self.graph_height
		self.treeVis.item_pos = -self.graph_leftmost, -self.graph_bottommost
		self.treeVis.ids['graph'].bounding_box = self.treeVis.graph_size[0], self.treeVis.graph_size[1]
		print self.treeVis.ids['graph'].bounding_box
		
		#Scale graph to fit in window#
		if self.treeVis.graph_width > self.treeVis.graph_height:
			self.treeVis.scale_index = (800 - self.border*2)/self.treeVis.graph_width
		else:
			self.treeVis.scale_index = (600 - self.border*2)/self.treeVis.graph_height
			
		
		#Center graph items#
		self.treeVis.graph.center= 400, 300

class GraphWidget(FloatLayout):
	
	global scale_treshold
	global zoom_speed
	
	def __init__(self, scale_index=None, **kwargs):
		super(GraphWidget,self).__init__(**kwargs)
		
		if there_is(scale_index):
			self.scale_index = scale_index
	
	def zoom_in(self, focus_pos):
		global zoom_in_limit
		print self.scale_index
		if self.scale_index + zoom_speed > zoom_in_limit: return
		
		focus_x, focus_y = focus_pos
		x_correction = ((focus_x - self.x)/self.width)*self.x_units*zoom_speed
		y_correction = ((focus_y - self.y)/self.height)*self.y_units*zoom_speed
		self.x -= x_correction
		self.y -= y_correction
		self.scale_index += zoom_speed
		print self, self.size
		
		print self.scale_index
		if self.scale_index > scale_treshold and self.parent.tags_hidden:
			print "SHOW TAGS"
			self.parent.show_tags()
		
	def zoom_out(self, focus_pos):
		global zoom_out_limit
		print self.scale_index
		if self.scale_index - zoom_speed < zoom_out_limit: return
		
		focus_x, focus_y = focus_pos
		x_correction = ((focus_x - self.x)/self.width)*self.x_units*zoom_speed
		y_correction = ((focus_y - self.y)/self.height)*self.y_units*zoom_speed
		self.x += x_correction
		self.y += y_correction
		self.scale_index -= zoom_speed
		print self, self.size
		
		if self.scale_index < scale_treshold and not self.parent.tags_hidden:
			print "HIDE TAGS"
			self.parent.hide_tags()
		
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
	graph_items = None
	screen = None
	tags_hidden = True
	
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
		self.graph_items = self.ids['graph_items']
		self.screen = self.ids['screen']
	
	def add_node(self, i, input_position, input_data=None):
		print "ADDING NODE", i
		new_node = Node(i, data=input_data, pos=input_position, radius=self.node_radius)
		new_node = Node(i, data=input_data, pos=input_position, radius=self.node_radius)
		self.node_widgets[i] = new_node
	
	def add_edge(self, i, input_tail, input_head, input_data=None):
		new_edge = Edge(i, data=input_data, tail=input_tail, head=input_head)
		new_edge = Edge(i, data=input_data, tail=input_tail, head=input_head)
		self.edge_widgets[i[1]]=new_edge
		
	def generate_tree(self):
		for part in (self.edge_widgets + self.node_widgets):
			if part != None:
				self.graph_items.add_widget(part)
				part.generate_info_text()
				part.generate_tag()
		self.show_tags()
		
		#By default, edge info is hidden for trees since all the data is in the nodes.
		if type(self.get_ctrl().graph_data) == Tree:
			self.get_ctrl().hide_etags()
	
	def show_tags(self):
		if self.tags_hidden:
			if not self.get_ctrl().ntags_hidden:
				for node in self.node_widgets:
					node.show_tag()
			if not self.get_ctrl().etags_hidden:
				for part in self.edge_widgets:
					if part != None:
						part.show_tag()
			self.tags_hidden = False
				
	def hide_tags(self):
		if not self.tags_hidden:
			for part in (self.edge_widgets + self.node_widgets):
				if part != None:
					part.hide_tag()
			self.tags_hidden = True
				
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
	ntags_hidden = False
	etags_hidden = False
	
	ctrl_down = False
	
	graph_data = None
	node_numAttrs = 0
	edge_numAttrs = 0
	
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
				print "CONTROL", self.ctrl_down
		if keycode[1] == 'd':
			print self.selection_1, self.selection_2
		if keycode[1] == 'n':
			if self.ctrl_down:
				self.rotate_ntags()
			else:
				self.toggle_ntag_visibility()
		if keycode[1] == 'e':
			if self.ctrl_down:
				self.rotate_etags()
			else:
				self.toggle_etag_visibility()
		return True
		
	def _on_keyboard_up(self, keyboard, keycode):
		if keycode[1] == 'lctrl':
			self.ctrl_down = False
			print "CONTROL", self.ctrl_down
		return True
	
	#GRAPH MANAGEMENT
	
	def take_graph_data(self, g):
		self.graph_data = g
		print self.graph_data.nodeAttrs
	
	def get_graph_node(self,i):
		print self.parent.visualizer.node_widgets[i], self.parent.visualizer.node_widgets[i].i
		return self.parent.visualizer.node_widgets[i]
		
	def get_graph_edge(self,i):
		print self.parent.visualizer.edge_widgets[i[1]], self.parent.visualizer.edge_widgets[i[1]].i
		return self.parent.visualizer.edge_widgets[i[1]]
	
	def hide_ntags(self):
		self.ntags_hidden = True
		if not self.get_visualizer().tags_hidden:
			for node in self.get_visualizer().node_widgets:
				node.hide_tag()
				
	def show_ntags(self):
		self.ntags_hidden = False
		if not self.get_visualizer().tags_hidden:
			for node in self.get_visualizer().node_widgets:
				node.show_tag()
				
	def toggle_ntag_visibility(self):
		if self.ntags_hidden:
			self.show_ntags()
		else:
			self.hide_ntags()
	
	def hide_etags(self):
		self.etags_hidden = True
		if not self.get_visualizer().tags_hidden:
			for edge in self.get_visualizer().edge_widgets:
				if edge != None: edge.hide_tag()
				
	def show_etags(self):
		self.etags_hidden = False
		if not self.get_visualizer().tags_hidden:
			for edge in self.get_visualizer().edge_widgets:
				if edge != None: edge.show_tag()
	
	def toggle_etag_visibility(self):
		if self.etags_hidden:
			self.show_etags()
		else:
			self.hide_etags()
		
	def rotate_ntags(self):
		for node in self.get_visualizer().node_widgets:
			node.rotate_tag()
		'''
		The tags weren't updating their position until the graph was moved. As a quick fix
		I've opted to 'nudge' the graph after rotating tags. This ought to only be temporary though.
		'''
		
		self.get_visualizer().graph.move((0.000000000001,0.000000000001))
		
	def rotate_etags(self):
		for edge in self.get_visualizer().edge_widgets:
			if edge != None: edge.rotate_tag()
		'''
		The tags weren't updating their position until the graph was moved. As a quick fix
		I've opted to 'nudge' the graph after rotating tags. This ought to only be temporary though.
		'''
		
		self.get_visualizer().graph.move((0.000000000001,0.000000000001))
		
	def select(self,item):
		if item.i in (self.selection_1, self.selection_2):
			print item.i, " is already selected"
			return
		elif self.selection_1 == None:
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
		
	def take_graph_data(self,g):
		self.control.take_graph_data(g)
	
	def get_ctrl(self):
		return self.control
			
class GraphVisApp(App):
    def build(self):
		
		t = load("OtherTGraph.txt")
		td = treeData(t)
		parent = WindowWidget()
		parent.take_graph_data(td.t)
		parent.take_visualizer(td.treeVis)
		td.load_tree()
		
		return parent

if __name__ == '__main__':
    GraphVisApp().run()

	
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
							graph_items(GraphItems): #Node layer#
				
As aforementioned, from just about any widget, the command "get_ctrl()" is available and returns Control.
'''
		