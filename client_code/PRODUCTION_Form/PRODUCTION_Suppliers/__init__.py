from ._anvil_designer import PRODUCTION_SuppliersTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Supplier_List import Supplier_List
from .Import_Card import Import_Card

class PRODUCTION_Suppliers(PRODUCTION_SuppliersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    cmpt = Supplier_List()
    self.content_panel.clear()
    self.content_panel.add_component(cmpt)
    
  
  def new_supplier_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers.New_Supplier_Card')
    pass

  def suppliers_list_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    cmpt = Supplier_List()
    self.content_panel.clear()
    self.content_panel.add_component(cmpt)
    pass

  def import_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    cmpt = Import_Card()
    self.content_panel.clear()
    self.content_panel.add_component(cmpt)
    pass

  def exit_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('PRODUCTION_Form')
    pass

  
