import os

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox

from pathlib import Path
from datetime import date

class ClaimScreen(Screen):

  def __init__(self, **kwargs):
    super(ClaimScreen, self).__init__(**kwargs)
    # initialize the following property values
    self.data_path = Path("data")
    self.cache = os.path.join(self.data_path, "cache.txt")
    self.date = date.today().strftime("%d %B %Y")

    # attach claim_screen_layout on self
    self.claim_screen_layout = BoxLayout(orientation="vertical")
    self.add_widget(self.claim_screen_layout)

    # attach claim_title_layout into claim_screen_layout
    self.claim_title_layout = BoxLayout(orientation = "vertical", size_hint = (1, 0.1))
    self.claim_screen_layout.add_widget(self.claim_title_layout)

    # attach claim_title_grid to scrollview_bubble
    self.claim_title_grid = GridLayout(cols=2)
    self.claim_title_layout.add_widget(self.claim_title_grid)

    # attach claim_title_label to claim_title_grid
    self.claim_title_label = Label(text=f"[b]Claim Screen ({self.date})[/b]", markup=True)
    self.claim_title_grid.add_widget(self.claim_title_label)

    # attach reload_button to claim_title_grid
    self.reload_button = Button(text='Reload Claims', size_hint_x=0.2, width=100)
    self.claim_title_grid.add_widget(self.reload_button)
    self.reload_button.bind(on_press=self.reload_claims)

    # scroll view here
    # attach scrollview to claim_screen_layout
    self.scrollview = ScrollView(size_hint=(1, 0.8))
    self.claim_screen_layout.add_widget(self.scrollview)

    # attach scrollview_layout to scrollview
    self.scrollview_layout = GridLayout(cols = 1, size_hint = (1, None))
    self.scrollview_layout.bind(minimum_height = self.scrollview_layout.setter("height"))
    self.scrollview.add_widget(self.scrollview_layout)

    # recover session data from data/cache.txt (just in case there was a restart/crash)
    # for each recovered session data, attach a label and a button
    self.load_from_cache()

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
    self.claim_button.bind(on_press = self.resolve_claim)

  def main_screen(self, instance):
    print('Accessing Main Sreen...')
    self.manager.transition.direction = "left"
    self.manager.current = "main_screen"

  def note_this_claim(self, checkbox, value):
    print(f'This claim id has been noted for claim: {checkbox.id}')
    self.noted_claim = checkbox.id

  def load_from_cache(self):
    print(f'Loading cache from {self.cache}...')

    # recover session data from data/cache.txt (just in case there was a restart/crash)
    # for each recovered session data, attach a label and a button

    self.claims = []
    with open(self.cache, 'r') as cache:
      for count, line in enumerate(cache):
        # build a list of claims
        self.claims.append(line)

        # format text accordingly here
        line = line.split(',')
        text = f"""
                  {line[0]} [Series] {line[2]}
                  {line[5]} Batches (Rounded) - {line[3]} kg. Total: Rp. {line[8]}
                ________________________________________________________________________
                """

        # attach scrollview_bubble to scrollview_layout
        self.scrollview_bubble = BoxLayout(orientation = "vertical", size_hint = (1, None))
        self.scrollview_layout.add_widget(self.scrollview_bubble)

        # attach scrollview_grid to scrollview_bubble
        self.scrollview_grid = GridLayout(cols=2)
        self.scrollview_bubble.add_widget(self.scrollview_grid)

        # attach cache_label to scrollview_layout
        self.cache_label = Label(text=text, halign='left', size_hint=(1.0, 1.0))
        self.cache_label.bind(size=self.cache_label.setter('text_size'))
        self.scrollview_grid.add_widget(self.cache_label)

        # attach cache_button to scrollview_layout
        self.cache_checkbox = CheckBox(group='unclaimed', size_hint_x=None, width=100, id=str(count))
        self.scrollview_grid.add_widget(self.cache_checkbox)
        self.cache_checkbox.bind(active=self.note_this_claim)

  def delete_cache_claim(self):
    with open(self.cache, "w") as cache:
      for i in range(len(self.claims)):
        if i != int(self.noted_claim):
            cache.write(self.claims[i])
    print(f'This claim (id: {self.noted_claim}) has been successfully resolved!')

  def resolve_claim(self, instance):
    # clear all claims first
    self.scrollview_layout.clear_widgets()

    # delete 1 entry in dictionary then update cache.txt
    self.delete_cache_claim()

    # reload from cache.txt
    self.load_from_cache()

  def reload_claims(self, instance):
    self.scrollview_layout.clear_widgets()
    self.load_from_cache()
    print(f'Claims have been reloaded!')

  def on_enter(self):
    self.scrollview_layout.clear_widgets()
    self.load_from_cache()
