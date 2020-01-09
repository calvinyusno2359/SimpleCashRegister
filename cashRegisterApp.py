import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from dotenv import load_dotenv
from pathlib import Path

# import the two screens
from loginScreen import LoginScreen
from mainScreen import MainScreen

class MyApp(App):

    def build(self):
        self.title = 'Cash Registry'
        sm = ScreenManager()

        # attach login_screen to screen manager
        login_screen = LoginScreen(name="login_screen")
        sm.add_widget(login_screen)

        # attach main_screen to screen manager
        main_screen = MainScreen(name="main_screen")
        sm.add_widget(main_screen)

        return sm

if __name__ == '__main__':

    # load .env into os (can be called with os.getenv('KEY'))
    env_path = Path(".env")
    load_dotenv(dotenv_path=env_path)

    MyApp().run()
