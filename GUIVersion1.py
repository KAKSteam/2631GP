# GUI Layout Version 1
# Creator: Robert Materi
# Partners: Mathieu & Blake

# Gets system tools
import sys

# Import Kivy tools
from kivy.app import App

# Provides drawable/interactable widgets
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.uix.checkbox import CheckBox

# Provides Graphical Primitives
from kivy.graphics import Color, Ellipse, Line

# Provides Tree and EWD Graph classes
from treelib import Tree
from treelib import Node
from pygraph.classes.digraph import digraph

# Provides helper methods in order to make the main code easier to read
class TreeHelper():
	@staticmethod
	def getCommonRoot(t,nid1,nid2):
	
		ancestorList1 = t.ancestors(nid1)
		ancestorList2 = t.ancestors(nid2)
		
		for a1 in ancestorList1:
			for a2 in ancestorList2:
				if (a1 == a2):
					return a1
		
		return None
		
	@staticmethod
	def getCommonSubTree(t,nid1,nid2):
	
		a = Helper.getCommonRoot(t,nid1,nid2)
		return t.subtree(a)
				
class GUICanvas(Widget):
	pass

class GUIApp(App):
	def build(self):
		
		menuBar = AnchorLayout(anchor_x='center', anchor_y='top')
		menuLayout = GridLayout(cols=3, size_hint=(1,0.1))

		self.painter = GUICanvas(size_hint=(1,0.9))
		
		# DropDown for Basic Menu
		menuDropDown = DropDown()
		loadBtn = Button(text='Load Graph', size_hint_y=None, height=50)
		clearBtn = Button(text='Clear Screen', size_hint_y=None, height=50)
		exitBtn = Button(text='Exit Program', size_hint_y=None, height=50)
		debugBtn = Button(text='Debug', size_hint_y=None, height=50)

		clearBtn.bind(on_release=self.clearCanvas)
		exitBtn.bind(on_release=self.exitApp)
		
		menuDropDown.add_widget(loadBtn)
		menuDropDown.add_widget(clearBtn)
		menuDropDown.add_widget(exitBtn)
		menuDropDown.add_widget(debugBtn)

		RegBtn = Button(text='Menu Bar')
		RegBtn.bind(on_release=menuDropDown.open)


		GraphToolBtn = Button(text='Graph Tools')
		lbl = Label(text='I Label')

		
		menuLayout.add_widget(RegBtn)
		menuLayout.add_widget(GraphToolBtn)
		menuLayout.add_widget(lbl)
		menuBar.add_widget(menuLayout)
		

		return menuBar

	def clearCanvas(self, obj):
		self.painter.canvas.clear()
		print 'Clearing Canvas!'

	def exitApp(self, obj):
		print 'Exitting'
		sys.exit(0)

	

GUIApp().run()