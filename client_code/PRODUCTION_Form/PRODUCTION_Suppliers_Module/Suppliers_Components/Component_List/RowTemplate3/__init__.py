from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.item_link.text = self.item['item_name']

  def details_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    supplier_id = self.item['supplier_id']
    cmpt_id = self.item['component_id']
    switch = self.item['is_commodity']

    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module.Suppliers_Components.Edit_Component', supplier_id, cmpt_id, switch)
    
    pass

  def item_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    supplier_id = self.item['supplier_id']
    cmpt_id = self.item['component_id']
    switch = self.item['is_commodity']

    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module.Suppliers_Components.Edit_Component', supplier_id, cmpt_id, switch)
    pass
