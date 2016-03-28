#!/usr/bin/env python
#Custom kivy widgets

#	this provides us drawable and interactable widgets
from kivy.uix.widget import Widget

#	this provides us graphical primitives
from kivy.graphics import Color, Ellipse

#import helper methods
from helper import there_is

#Round Button is intended to function just like other
#buttons found in Kivy, only the click region is circular.

defaultColor = (.4, .7, 1)

class CircularButton(Widget):

	#Instance Variables#
	functions = []
	#axis = (0,0)
	radius = 0
	main_color = defaultColor
	#color
	
	#state variable: 3 modes: "pressed" "idle" "enter"
	state = "idle"

	#Initializer#
	def __init__(self, input_pos=None,input_radius=None,input_color=None, input_functions=None, **kwargs):
		super(CircularButton,self).__init__(**kwargs)
		
		#self.size_hint = (None,None)
		#self.pos_hint = (None,None)
		#self.pos = self.pos
		#self.axis = tuple([x for x in self.center])
		self.radius = self.width
		#self.boun
		print self.size, self.radius, self.pos, self.center
		
		#Check for optional input values
		if there_is(input_color): #TODO: check if valid color
			self.main_color = input_color
		if there_is(input_functions):
			if isinstance(input_functions,list): #TODO: check if valid functions
				self.functions = input_functions
			else:
				self.functions.append(input_functions)
		
		self.drawButton()
		print self.pos

	def on_touch_down(self, touch):
		if self.collide_point(touch.x,touch.y):
			self.state = "pressed"
			self.drawButton()
			print self.pos, self.size
		
	def on_touch_up(self, touch):
		self.state = "idle"
		self.drawButton
		print "UP"
		
	def drawButton(self):
		#print self.size, self.center
		x, y = self.center
		with self.canvas:
			if self.state == "idle":
				Color(*self.main_color)
				Ellipse(pos=(x - self.radius / 2, y - self.radius / 2), size=(self.radius, self.radius))
			
			if self.state == "enter":
				c = tuple([1.5*v for v in self.main_color])
				Color(*c)
				Ellipse(pos=(x - self.radius / 2, y - self.radius / 2), size=(self.radius, self.radius))
			
			if self.state == "pressed":
				c = tuple([0.75*v for v in self.main_color])
				Color(*c)
				Ellipse(pos=(x - self.radius / 2, y - self.radius / 2), size=(self.radius, self.radius))
			
			
	#better idea, make widget for tree that will be composed of nodes and edges so you can move and scale
	#then, have your handler/controller what evs with the info