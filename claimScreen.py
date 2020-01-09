from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

class ClaimScreen(Screen):

  def __init__(self, **kwargs):
    super(ClaimScreen, self).__init__(**kwargs)

    # attach claim_screen_layout on self
    self.claim_screen_layout = BoxLayout(orientation="vertical")
    self.add_widget(self.claim_screen_layout)

    # attach claim_title_layout into claim_screen_layout
    self.claim_title_layout = BoxLayout(orientation = "vertical", size_hint = (1, 0.1))
    self.claim_screen_layout.add_widget(self.claim_title_layout)

    # attach claim_title_label to claim_title_layout
    self.claim_title_label = Label(text="Claim Screen")
    self.claim_title_layout.add_widget(self.claim_title_label)

    # scroll view here
    # attach scrollview to claim_screen_layout
    self.scrollview = ScrollView(size_hint=(1, 0.8))
    self.claim_screen_layout.add_widget(self.scrollview)

    # attach scrollview_layout to scrollview
    self.scrollview_layout = GridLayout(cols = 1, size_hint = (1, None))
    self.scrollview_layout.bind(minimum_height = self.scrollview_layout.setter("height"))

    # recover session data from data/cache.txt (just in case there was a restart/crash)
    # for each recovered session data, attach a label and a button

    # buttons here
    # attach claim_button_layout to claim_screen_layout
    self.claim_button_layout = GridLayout(cols = 2, size_hint = (1, 0.1))
    self.claim_screen_layout.add_widget(self.claim_button_layout)

    # attach main_screen_button on claim_button_layout
    self.main_screen_button = Button(text='Main Screen')
    self.claim_button_layout.add_widget(self.main_screen_button)
    self.main_screen_button.bind(on_press = self.main_screen)

    # attach claim_button on claim_button_layout
    self.claim_button = Button(text='Claim')
    self.claim_button_layout.add_widget(self.claim_button)
    self.claim_button.bind(on_press = self.main_screen)

  def main_screen(self, instance):
    print('Accessing Main Sreen...')
    self.manager.transition.direction = "left"
    self.manager.current = "main_screen"

