
# get system tools
import sys

# import kivy tools
#	this is a "root window" application
from kivy.app import App

#	this provides us drawable and interactable widgets
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

#	this provides us graphical primitives
from kivy.graphics import Color, Ellipse, Line

# this isn't part of kivy, but allows us access to random numbers
from random import random

	# floating point 20 for touch diameter
touchDiameter = 20.

class MyPaintWidget(Widget):
	def on_touch_down(self, touch):
		# create a random colour
		color = (0.25 + random()/0.75,
				 random()/0.25,
				 random()/0.25)

		with self.canvas:
			Color(*color)
			d = touchDiameter
			Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))

			# touch.ud is a 'user dictionary' attached to the touch object
			# use it to remember a Line(points=(x,y), width=yourwidth)
			# object...
			#
			# touch.ud['line'] =
			touch.ud['line'] = Line(points=(touch.x, touch.y), width=d/3)
			#touch.ud['line'] = Line(points=(touch.x, touch.y))

	def on_touch_move(self, touch):
		touch.ud['line'].points += [touch.x, touch.y]

	def on_touch_up(self, touch):
		with self.canvas:
			d = touchDiameter
			Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d/2, d/2))


class MyPaintApp(App):
	def build(self):

		parent = BoxLayout()
		self.painter = MyPaintWidget(size_hint=(0.9,1))

		buttonPanel = BoxLayout(orientation='vertical', size_hint=(0.1,1))
		btnClear = Button(text='Clear')
		btnExit = Button(text='Exit')

		# register clearCanvas() as the _callback_ for this button
		btnClear.bind(on_release=self.clearCanvas)
		btnExit.bind(on_release=self.exitApp)

		parent.add_widget(self.painter)
		buttonPanel.add_widget(btnClear)
		buttonPanel.add_widget(btnExit)
		parent.add_widget(buttonPanel)
		return parent

	def clearCanvas(self, obj):
		self.painter.canvas.clear()
		print 'Clearing canvas!'

	def exitApp(self, obj):
		print 'Exitting'
		sys.exit(0)


MyPaintApp().run()
