import sys
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

#GRAPH PAINTER

def paintGraph():

class MyVisWidget(Widget):
	#
	num = 0
	#

class MyPaintApp(App):
	def build(self):
		parent = BoxLayout()
		vis = MyVisWidget(size_hint(1,1))