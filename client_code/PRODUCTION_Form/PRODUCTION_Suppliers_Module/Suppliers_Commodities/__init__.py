from ._anvil_designer import Suppliers_CommoditiesTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Commodity_List import Commodity_List

class Suppliers_Commodities(Suppliers_CommoditiesTemplate):
  def __init__(self,supplier_id = None,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id 

    # Any code you write here will run before the form opens.
    cmpt = Commodity_List(self.supplier_id)
    self.content_panel.clear()
    self.content_panel.add_component(cmpt)

  def new_commodity_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module.Suppliers_Commodities.New_Commodity', self.supplier_id)
    pass

  def exit_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module.Suppliers_Components', self.supplier_id)
    pass
    
