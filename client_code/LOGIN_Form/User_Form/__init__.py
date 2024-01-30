from ._anvil_designer import User_FormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class User_Form(User_FormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    #hello world

  def save_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    company_name = self.company_name_text_box.text 
    first_name = self.first_name_textbox.text
    last_name = self.last_name_textbox.text

    if first_name == "" or last_name == "" or company_name == "":
      anvil.alert("Please fill all text fields")
    else:
      anvil.server.call('new_company',company_name, first_name, last_name)
      open_form('LANDING_Form')

    pass
