import os
import pandas as pd

from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

from base64 import b64encode

class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        Window.size = (600, 300)

        # attach grid_layout on screen
        self.grid_layout = GridLayout(cols=2)
        self.add_widget(self.grid_layout)

        # attach username_label on grid_layout
        self.username_label = Label(text='User Name')
        self.grid_layout.add_widget(self.username_label)

        # attach username text value on grid_layout
        self.grid_layout.username = TextInput(multiline=False)
        self.grid_layout.add_widget(self.grid_layout.username)

        # attach password_label on grid_layout
        self.password_label = Label(text='Password')
        self.grid_layout.add_widget(self.password_label)

        # attach password text value on grid_layout
        self.grid_layout.password = TextInput(password=True, multiline=False)
        self.grid_layout.add_widget(self.grid_layout.password)

        # attach reset_button on grid_layout
        self.reset_button = Button(text='Reset')
        self.grid_layout.add_widget(self.reset_button)
        self.reset_button.bind(on_press = self.reset)

        # attach confirm_button on grid_layout
        self.confirm_button = Button(text='Confirm')
        self.grid_layout.add_widget(self.confirm_button)
        self.confirm_button.bind(on_press = self.authenticate)

    # callback methods here

    def reset(self):
        self.grid_layout.username.text = ""
        self.grid_layout.password.text = ""

    def authenticate(self, instance):
        self.check(self.grid_layout.username.text, self.grid_layout.password.text)

    def check(self, username, password):
        true_username = os.getenv("USER_NAME")[4:]
        true_password = os.getenv("PASSWORD")[4:]

        encoded_username = str(b64encode(username.encode("utf-8")), "utf-8")
        encoded_password = str(b64encode(password.encode("utf-8")), "utf-8")

        if encoded_username == true_username and encoded_password == true_password:
            print('Authentication successful!')

            # open MainScreen
            Window.size = (900, 700)
            self.manager.transition.direction = "right"
            self.manager.current = "main_screen"

        else:
            print('Wrong Username and/or Password!')
            self.reset()
