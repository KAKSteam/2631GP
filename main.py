import sys
import os

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.bubble import Bubble
from kivy.uix.bubble import BubbleButton


class RootWidget(FloatLayout):
    load = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def exit_App(self):
        print "Leaving Program"
        sys.exit(0)

    def dismiss_Popup(self):
        self._popup.dismiss()

    def show_Load(self):
        content = LoadGraph(load=self.load, cancel=self.dismiss_Popup)
        self._popup = Popup(title="Load Graph file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
        self.dismiss_Popup()

    def on_touch_up(self, touch):
        if touch.button == "right":
            x = touch.x
            y = touch.y
            graphtools = GraphTools(orientation="vertical", size_hint=(None, None), pos=(touch.x, touch.y), size=(200, 120), show_arrow=False)
            self.add_widget(graphtools)

class GraphTools(Bubble):
    def __init__(self, **kwargs):
        super(GraphTools, self).__init__(**kwargs)
        Path = BubbleButton(text="Highlight Path to Root")
        self.add_widget(Path)
        Subtree = BubbleButton(text="Highlight Subtree")
        self.add_widget(Subtree)
        Depth = BubbleButton(text="Highlight Same Depth")
        self.add_widget(Depth)

		
class LoadGraph(FloatLayout):
    loadfile = ObjectProperty(None)
    cancel = ObjectProperty(None)
    text_input = ObjectProperty(None)
    
    def dismiss_Popup(self):
        self._popup.dismiss()

    def show_Load(self):
        content = LoadGraph(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load Graph file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
        self.dismiss_Popup()


class MainApp(App):
    
    def build(self):
        '''Your app will be build from here.
           Return your root widget here.
        '''
        print('build running')
        return RootWidget()

    def on_pause(self):
        '''This is necessary to allow your app to be paused on mobile os.
           refer http://kivy.org/docs/api-kivy.app.html#pause-mode .
        '''
        return True

#Factory.register('LoadDialog', cls=LoadDialog)
#Factory.register('

if __name__ == '__main__':
    MainApp().run()

