from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.graphics.transformation import Matrix
from kivy.uix.floatlayout import FloatLayout
from helper import zero_patch, there_is
from loader import load
from kivy.uix.bubble import Bubble

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

#Object holding relevant data for visualizing the tree
class treeData():

	t = None
	treeVis = None
	axis = [3,1]
	offset = []

	def __init__(self, tree):
		global left
		global right

		#Load tree
		self.t = tree
		self.treeVis = TreeVisualizer()
		
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
		
		#Add the offset of the node under consider
		pos = [root_x + offset[nid], root_y]
		
		#If not root, move the node down by the scale value
		if nid != 0: pos[1] -= 1
		
		#paint the node and the edge leading up to it
		self.treeVis.add_node(pos)
		if nid != 0: self.treeVis.add_edge(root_pos,pos) #only print the edge if it is not a root
		for cid in t.get_node(nid).fpointer:
			self.drawTree(cid, pos) #call drawTree on children

class PopUp(Bubble):
	pass

class ExtendedInit(type):
	def __call__(cls, *args, **kwargs):
		obj = type.__call__(cls, *args, **kwargs)
		obj.post_init()
		return obj

class GraphWidget(Scatter):
	grow_scaler = Matrix().scale(1.1,1.1,1)
	shrink_scaler = Matrix().scale(0.9,0.9,1)
	
	def __init__(self, scale_index=None, **kwargs):
		super(GraphWidget,self).__init__(**kwargs)
		
		if there_is(scale_index):
			self.scale_index = scale_index
		
		self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
		self._keyboard.bind(on_key_down=self._on_keyboard_down)
	
	def zoom_in(self, focus_pos):
		self.apply_transform(self.grow_scaler, anchor=focus_pos)
		
	def zoom_out(self, focus_pos):
		self.apply_transform(self.shrink_scaler, anchor=focus_pos)
		
	def move(self, transform_vector):
		delta_x, delta_y = transform_vector
		self.center_x += delta_x
		self.center_y += delta_y
	
	def _keyboard_closed(self):
		self._keyboard.unbind(on_key_down=self._on_keyboard_down)
		self._keyboard = None
		
	def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
		if keycode[1] == 'right':
			self.center_x += dragSpeed
		elif keycode[1] == 'left':
			self.center_x -= dragSpeed
		elif keycode[1] == 'down':
			self.apply_transform(self.shrink_scaler)
		elif keycode[1] == 'up':
			self.apply_transform(self.grow_scaler)
		return True
	
class GraphItems(FloatLayout):

	def __init__(self, scale_index=None, **kwargs):
		super(GraphItems,self).__init__(**kwargs)
		
		if there_is(scale_index):
			self.scale_index = scale_index

class Node(FloatLayout):
	def __init__(self, color=None, **kwargs):
		super(Node,self).__init__(**kwargs)
		self.pos_x, self.pos_y = self.pos
		
		if there_is(color):
			self.color = color

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
	'''
		print self.width
		self.x_scale = self.width
		self.y_scale = self.height
		
		if self.head_x == self.tail_x:
			self.x_scale = 0
			self.handle_x = 0
		if self.head_y == self.tail_y:
			self.y_scale = 0
			self.handle_y = 0
	def __call__(self):
		print self.width
	'''
		
class TreeVisualizer(Widget):
	graph = None
	graph_items = None
	screen = None
	
	node_radius = 1
	
	def __init__(self, **kwargs):
		super(TreeVisualizer, self).__init__(**kwargs)
		self.graph = self.ids['graph']
		self.graph_items = self.ids['graph_items']
		self.screen = self.ids['screen']
	
	def add_node(self, input_position):
		new_node = Node(pos=input_position, radius=self.node_radius)
		self.graph_items.add_widget(new_node)
	
	def add_edge(self, input_tail, input_head):
		new_edge = Edge(tail=input_tail, head=input_head)
		self.graph_items.add_widget(new_edge)

class ScreenWidget(Widget):
	def on_touch_down(self,touch):
		if touch.button == 'middle':
			touch.grab(self)
		elif touch.button == 'scrollup':
			self.parent.graph.zoom_in(touch.pos)
		elif touch.button == 'scrolldown':
			self.parent.graph.zoom_out(touch.pos)
			
	def on_touch_move(self, touch):
		if touch.grab_current is self:
			x, y = touch.pos
			x0, y0 = touch.ppos
			transform_vector = (x-x0, y-y0)
			self.parent.graph.move(transform_vector)
			
	def on_touch_up(self, touch):
		if touch.grab_current is self:
			touch.ungrab(self)

class TreeVisApp(App):
    def build(self):
		
		t = load("TGraphFinal.txt")
		td = treeData(t)
		td.drawTree()
		
		parent = FloatLayout()
		parent.add_widget(td.treeVis)
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