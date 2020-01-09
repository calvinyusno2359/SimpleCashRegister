import os
import math
import pandas as pd

from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window

from pathlib import Path
from base64 import b64encode
from datetime import date

class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # initialize the following property values
        self.data_path = Path("data")
        self.cache = os.path.join(self.data_path, "cache.txt")
        self.date = date.today().strftime("%d %B %Y")
        self.index = 1
        print('Initializing system for today: {}'.format(self.date))
        print('Data storage path: {}'.format(self.data_path))

        # the following property values
        self.batch = 0
        self.rounded_batch = 0
        self.option = 0
        self.option_price = 0
        self.total_price_value = 0
        self.return_value = 0
        print('Completed Intialization.')

        # attach grid_layout on screen
        self.grid_layout = GridLayout(cols=2)
        self.add_widget(self.grid_layout)

        # attach exit_button on grid_layout
        self.exit_button = Button(text='Exit')
        self.grid_layout.add_widget(self.exit_button)
        self.exit_button.bind(on_press = self.exit)

        # attach claim_screen_button on grid_layout
        self.claim_screen_button = Button(text='Claim Screen')
        self.grid_layout.add_widget(self.claim_screen_button)
        self.claim_screen_button.bind(on_press = self.claim_screen)

        # attach date_label on grid_layout
        self.date_label = Label(text="{}".format(self.date))
        self.grid_layout.add_widget(self.date_label)

        # attach index_label on grid_layout
        self.index_label = Label(text="Customer No. {}".format(self.index))
        self.grid_layout.add_widget(self.index_label)

        # attach name_label on grid_layout
        self.name_label = Label(text='Customer Name (Nama Pelanggan)')
        self.grid_layout.add_widget(self.name_label)

        # attach name text value on grid_layout
        self.grid_layout.name = TextInput(multiline=False)
        self.grid_layout.add_widget(self.grid_layout.name)

        # attach weight_label on grid_layout
        self.weight_label = Label(text='Weight (Berat) /kg')
        self.grid_layout.add_widget(self.weight_label)

        # attach weight text value on grid_layout + bind a callback to it
        self.grid_layout.weight = TextInput(multiline=False, input_filter="float", hint_text="20.7")
        self.grid_layout.add_widget(self.grid_layout.weight)
        self.grid_layout.weight.bind(text = self.show_batch_value)

        # attach batch_label on grid_layout
        self.batch_label = Label(text='Batch (Tabung) - per {} kg'.format(os.getenv("BATCH_LIMIT")))
        self.grid_layout.add_widget(self.batch_label)

        # attach batch_value_label on grid_layout
        self.batch_value_label = Label(text='')
        self.grid_layout.add_widget(self.batch_value_label)

        # attach option_label on grid_layout
        self.option_label = Label(text='Options')
        self.grid_layout.add_widget(self.option_label)

        # attach option_layout on grid_layout
        self.option_layout = BoxLayout(orientation = "horizontal")
        self.grid_layout.add_widget(self.option_layout)

        # for each option, attach a button on option_layout
        self.OPTIONS = os.getenv("OPTIONS").split(",")
        for option in self.OPTIONS:
            self.option_button = ToggleButton(text=option, group='options')
            self.option_layout.add_widget(self.option_button)
            self.option_button.bind(state = self.show_option_price)

        # attach calculation_label on grid_layout
        self.calculation_label = Label(text='Calculation')
        self.grid_layout.add_widget(self.calculation_label)

        # attach calculation_value_label on grid_layout
        self.calculation_value_label = Label(text='')
        self.grid_layout.add_widget(self.calculation_value_label)

        # attach total_price_label on grid_layout
        self.total_price_label = Label(text='Total Price /Rp')
        self.grid_layout.add_widget(self.total_price_label)

        # attach total_price_value_label on grid_layout
        self.total_price_value_label = Label(text='')
        self.grid_layout.add_widget(self.total_price_value_label)

        # attach payment_label on grid_layout
        self.payment_label = Label(text='Payment (Dibayar) /Rp')
        self.grid_layout.add_widget(self.payment_label)

        # attach payment text value on grid_layout
        self.grid_layout.payment = TextInput(multiline=False, input_filter="float", hint_text="25000")
        self.grid_layout.add_widget(self.grid_layout.payment)
        self.grid_layout.payment.bind(text = self.show_return_value)

        # attach return_label on grid_layout
        self.return_label = Label(text='Return (Kembali) /Rp')
        self.grid_layout.add_widget(self.return_label)

        # attach return_value_label on grid_layout
        self.return_value_label = Label(text='')
        self.grid_layout.add_widget(self.return_value_label)

        # attach reset_button on grid_layout
        self.reset_button = Button(text='Reset')
        self.grid_layout.add_widget(self.reset_button)
        self.reset_button.bind(on_press = self.reset)

        # attach confirm_button on grid_layout
        self.confirm_button = Button(text='Confirm')
        self.grid_layout.add_widget(self.confirm_button)
        self.confirm_button.bind(on_press = self.commit)

    # callback methods here

    def exit(self, instance):
        print('Exiting Application...')

        self.reset(instance)

        Window.size = (600, 300)
        self.manager.transition.direction = "left"
        self.manager.current = "login_screen"


    def claim_screen(self, instance):
        print('Accessing Claim Sreen...')
        self.manager.transition.direction = "right"
        self.manager.current = "claim_screen"

    def reset(self, instance):
        # reset text input > will automatically call the appropriate callbacks and reset labels
        self.grid_layout.name.text = ""
        self.grid_layout.weight.text = ""
        self.grid_layout.payment.text = ""

    def show_batch_value(self, instance, weight):
        if weight == "": weight = 0

        # update batch and rounded_batch values
        self.batch = float(weight) / float(os.getenv("BATCH_LIMIT"))
        self.rounded_batch = math.ceil(self.batch)

        # update BOTH batch_value_label and calculation_value_label (the part that has rounded_batch)
        # print("Batch calculated as {} rounded to {}".format(self.batch, self.rounded_batch))
        self.batch_value_label.text = "{} batch(es)".format(self.rounded_batch)
        self.calculation_value_label.text = "{} x Rp. {}".format(self.rounded_batch, self.option_price)

        self.show_total_price_value(instance, self.rounded_batch, self.option_price)
        self.show_return_value(instance, self.grid_layout.payment.text)

    def show_option_price(self, instance, state):
        # if a toggle exists ("down"): get price of selected option, overriding initialized value of 0
        if state == "down":
            self.option = instance.text
            self.option_price = int(os.getenv(instance.text))

            # print('Option <{}> is selected with price: Rp. {}'.format(instance.text, self.option_price))

            # update calculation_value_label text (the part that has option_price)
            self.calculation_value_label.text = "{} x Rp. {}".format(self.rounded_batch, self.option_price)

            self.show_total_price_value(instance, self.rounded_batch, self.option_price)
            self.show_return_value(instance, self.grid_layout.payment.text)

        # if not ("normal"), then reinitialize option_price to 0, still calculate with option_price = 0
        else:
            self.option = 0
            self.option_price = 0
            # print('Option <{}> is deselected.'.format(instance.text))

            # update calculation_value_label text (the part that has option_price)
            self.calculation_value_label.text = "{} x Rp. {}".format(self.rounded_batch, self.option_price)

            self.show_total_price_value(instance, self.rounded_batch, self.option_price)
            self.show_return_value(instance, self.grid_layout.payment.text)

    def show_total_price_value(self, instance, batch, option_price):
        # recalculate total price and update total_price_value_label text
        self.total_price_value = self.rounded_batch * self.option_price
        self.total_price_value_label.text = "Rp. {}".format(self.total_price_value)

    def show_return_value(self, instance, payment):
        if payment == "": payment = 0
        # recalculate return_value and update its label accordingly
        self.return_value = int(payment) - self.total_price_value
        self.return_value_label.text = "Rp. {}".format(self.return_value)

    def commit(self, instance):
        # get validation
        validation = self.get_validation()
        if validation == False:
            print("Validation has failed! This customer data is not registered.")

        else:
            # if validation == True append new_row to the correct book_path
            book_path, df, label = self.get_current_month_book()
            value_list = [str(self.date),
                          str(self.index),
                          str(self.grid_layout.name.text),
                          str(self.grid_layout.weight.text),
                          str(self.batch),
                          str(self.rounded_batch),
                          str(self.option),
                          str(self.option_price),
                          str(self.total_price_value),
                          str(self.grid_layout.payment.text),
                          str(self.return_value)]

            new_row = dict(zip(label, value_list))
            df = df.append(new_row, ignore_index=True)
            df.to_excel(book_path, index=False)
            print('Committing {} to {}'.format(value_list, book_path))

            # write to cache as txt, this is read by claimScreen later on
            with open(self.cache, 'a') as cache:
                line = ','.join(value_list)
                cache.write(f'{line}' + '\n')
                print(f'Also recorded in {self.cache}')

            # reset for next customer
            print('Customer {} has been recorded!'.format(self.index))
            self.reset(instance)

            # update customer index
            self.index += 1
            self.index_label.text = "Customer No. {}".format(self.index)

    def get_current_month_book(self):
        # check if this month's book exist, if not create one
        self.date = date.today().strftime("%d %B %Y")
        book_title = "{}.xlsx".format(date.today().strftime("%B %Y"))
        label = [ 'Date',
                  'Index',
                  'Name',
                  'Weight',
                  'Batch',
                  'Batch (Rounded)',
                  'Option',
                  'Option Price',
                  'Total Price',
                  'Payment',
                  'Return' ]

        if book_title in os.listdir(self.data_path):
            print('Loading {} in {}'.format(book_title, self.data_path))
            book_path = os.path.join(self.data_path, book_title)
            df = pd.read_excel(book_path, index=False)
            return book_path, df, label
        else:
            print('Creating {} in {}'.format(book_title, self.data_path))
            book_path = os.path.join(self.data_path, book_title)
            df = pd.DataFrame(columns=label)
            df.to_excel(book_path, index=False)
            return book_path, df, label

    def get_validation(self):
        if len(self.grid_layout.weight.text) == 0:
            print("No weight specified (kg).")
            return False
        elif self.rounded_batch == 0 or self.batch == 0:
            print("0 Batches registered. There may be an error with script, please restart.")
            return False
        elif self.option == 0:
            print("No option selected.")
            return False
        elif self.option_price == 0:
            print("Option Price is 0. There may be an error when setting Option Price in .env file.")
            return False
        elif len(self.grid_layout.payment.text) == 0:
            print("Payment value hasn't been specified.")
            return False
        elif self.return_value < 0:
            print("Total Price exceeds payment. Please get more payment.")
            return False
        else: return True


