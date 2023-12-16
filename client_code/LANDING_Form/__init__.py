from ._anvil_designer import LANDING_FormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from .. import main_functions_cache

class LANDING_Form(LANDING_FormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    company = main_functions_cache.get_company_name()
    self.company_label.text = company['company_name']
    
    

  def production_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('PRODUCTION_Form')
    pass

  def log_out_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    main_functions_cache.clear_all_caches()
    anvil.users.logout()
    open_form('LOGIN_Form')
    pass
