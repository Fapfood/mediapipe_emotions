from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.graphics import Rectangle, Color
from kivy.uix.camera import Camera
from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp



# use kv file for widgets seetings
Builder.load_file('images.kv')

# define default resolution
Config.set('graphics', 'width', '1440')
Config.set('graphics', 'height', '950')

# Create the screen manager
class ScreenManagement(ScreenManager):
    pass

# Declare home screen
class HomeScreen(Screen):
    pass

# Declare settings screen
class SettingsScreen(Screen):
    def func_abc(self, instance):
        print(f"func_abc: Called from Button with text={instance.text}") # example how to use class inside kv and Py

# Declare view screen
class ViewScreen(Screen):
    pass

# Create the app
class Face(MDApp):
	def build(self):
		return ScreenManagement()

if __name__ == '__main__':
	Face().run()













