from ._anvil_designer import PRODUCTION_Suppliers_ModuleTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Edit_Supplier_Card import Edit_Supplier_Card


class PRODUCTION_Suppliers_Module(PRODUCTION_Suppliers_ModuleTemplate):
  def __init__(self, supplier_id =None, supplier_name = None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id
    self.supplier_label.text = supplier_name
    
    # Any code you write here will run before the form opens.
    cmpt = Edit_Supplier_Card(supplier_id)
    self.content_panel.clear()
    self.content_panel.add_component(cmpt)
    

  def exit_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers')
    pass

  def components_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module.Suppliers_Components', self.supplier_id)
    pass

  def po_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Purchase_Orders', self.supplier_id)
    pass

  def commodity_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module.Suppliers_Commodities')
    pass
    
