import sys
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse, Line
from loader import load
from FDG import FDG, sLoad

defaultEdgeThickness = 2
defaultColor = (.4, .7, 1)
daxis = [320,300]
dscale = 40
defaultDiam = 20

def loadG(path):
	return sLoad(path)

class VisWidget(Widget):
 	
	G,x = loadG("att.txt")
	#nodeImage = []
	#edgeImage = []
			
	def node(self, pos, col=defaultColor):
		x, y = pos
		color = col

		with self.canvas:
			Color(*color)
			d = defaultDiam
			Ellipse(pos=(x - d / 2, y - d / 2), size=(d, d))

	def edge(self, pos1, pos2, col = defaultColor, 	edgeThickness = defaultEdgeThickness):
		x1, y1 = pos1
		x2, y2 = pos2
		color = col

		with self.canvas:
			Color(*color)
			d = defaultDiam
			Line(points=[x1,y1,x2,y2], width = edgeThickness)
			
	def draw(self, nid=0, altroot_pos=None):
		#Draws a single node and the edge leading up to it (unless is a root), and then
		#calls it's self on its children.
		
		#for it in x:
	
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
	
class MyVisApp(App):
	def build(self):
		parent = BoxLayout()
		#x = loadG("EWDGraphFinal.txt")
		graph = VisWidget()
		#graph.draw()
		
		#pos1 = (100,100)
		#pos2 = (120,300)
		
		#self.tree.node(pos1,defaultColor)
		#self.tree.node(pos2,defaultColor)
		#self.tree.edge(pos1,pos2,defaultColor)

		#parent.add_widget(graph)
		return parent

	def clearCanvas(self, obj):
		self.painter.canvas.clear()
		print 'Clearing canvas!'
		
MyVisApp().run()