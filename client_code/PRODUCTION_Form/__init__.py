from ._anvil_designer import PRODUCTION_FormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .PRODUCTION_Suppliers.Import_Card import Import_Card

class PRODUCTION_Form(PRODUCTION_FormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.


  #___ Perform Side Bar Link Functions
  def suppliers_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers')
    pass

  def exit_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('LANDING_Form')
    pass


    