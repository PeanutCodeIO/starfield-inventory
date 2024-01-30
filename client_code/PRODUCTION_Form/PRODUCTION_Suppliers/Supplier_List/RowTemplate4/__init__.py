from ._anvil_designer import RowTemplate4Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import component_cache
from ..... import supplier_cache

class RowTemplate4(RowTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.business_name_link.text = self.item['business_name']
    

  def details_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    component_cache.refresh_supplier_components()
    supplier_cache.refresh_purchase_orders()
    
    supplier_id = self.item['supplier_id']
    supplier_name = self.item['business_name']
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module', supplier_id, supplier_name)
    pass

  def business_name_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    component_cache.refresh_supplier_components()
    supplier_cache.refresh_purchase_orders()
    
    supplier_id = self.item['supplier_id']
    supplier_name = self.item['business_name']
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module', supplier_id, supplier_name)
    pass
