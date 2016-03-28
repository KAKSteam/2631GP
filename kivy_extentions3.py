#!/usr/bin/env python
#Custom kivy widgets

#	this provides us drawable and interactable widgets
from kivy.uix.widget import Widget

#	this provides us graphical primitives
from kivy.graphics import Color, Ellipse
from kivy.uix.image import Image

#import helper methods
from helper import there_is

#The functional components of the circular button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button

#Round Button is intended to function just like other
#buttons found in Kivy, only the click region is circular.

defaultColor = (.4, .7, 1)
infinitesimal = 0.000000000000000000000000000000001
infinite = 1000000000000000000000000000000000

class CircleImage(Image):
	def __init__(self, **kwargs):
		super(CircleImage, self).__init__(**kwargs)
		
		global infinitesimal
		global infinite
		
		self.pos = (100,100)
		self.size_hint = (None,None)
		self.size = (50,50)
		
		with self.canvas:
			self.opacity = infinitesimal
			Color(*defaultColor)
			Ellipse(pos=(100,100),size=(50,50),opacity=infinite)
			
			#Ellipse(pos=(100,100),size=(50,50),color=(1,1,1,1))
			
			#Ellipse(pos=(100,100),size=(50,50),color=(1,1,1,1))
			
			#Ellipse(pos=(100,100),size=(50,50),color=(1,1,1,1))
			
			#Ellipse(pos=(100,100),size=(50,50),color=(1,1,1,1))
			
			#Ellipse(pos=(100,100),size=(50,50),color=(1,1,1,1))

class CircularButton(Button):

	def __init__(self, **kwargs):
		super(CircularButton, self).__init__(**kwargs)
		self.background_color=(0,0,0)
		#self.draw()

	def yo(self):
		print "yo"
	
	def on_press(self):
		self.yo()
		self.parent.mytest.thing()
		
	def draw(self):
		with self.canvas:
			#self.parent.do_layout()
			Color(*defaultColor)
			Ellipse(pos=self.pos,size=self.size)
			
	#better idea, make widget for tree that will be composed of nodes and edges so you can move and scale
	#then, have your handler/controller what evs with the info