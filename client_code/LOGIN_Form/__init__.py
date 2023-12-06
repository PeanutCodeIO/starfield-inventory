from ._anvil_designer import LOGIN_FormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

class LOGIN_Form(LOGIN_FormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def login_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    # Attempt to log in the user
    user = anvil.users.login_with_form(show_signup_option=False, allow_remembered=True, allow_cancel=True)
    
    # Check if the user is successfully logged in
    if user:
        # Check if the name is filled
        name_filled = anvil.server.call('is_name_filled')
        
        # Redirect based on whether the name is filled
        if not name_filled:
            open_form('LOGIN_Form.User_Form')
        else:
            open_form('LANDING_Form')
    else:
        # Handle the case where no user is logged in after the login attempt
        # This could be displaying a message, or simply doing nothing
        pass


  def sign_up_link_click(self, **event_args):
    """This method is called when the link is clicked"""

    register = anvil.users.signup_with_form(allow_cancel=True, remember_by_default=True)
    name_filled = anvil.server.call('is_name_filled')
    if register:
      if name_filled != True:
        open_form('LOGIN_Form.User_Form')
      else:
        open_form('LANDING_Form')
    pass
