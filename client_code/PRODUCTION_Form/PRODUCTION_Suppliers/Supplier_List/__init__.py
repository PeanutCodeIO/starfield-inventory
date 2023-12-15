from ._anvil_designer import Supplier_ListTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import supplier_cache


class Supplier_List(Supplier_ListTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    suppliers = supplier_cache.get_all_suppliers()
    self.repeating_panel_suppliers.items = suppliers
    

  def search_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    search_term = self.search_text_box.text.lower()
    all_suppliers = supplier_cache.get_all_suppliers()
    
    filtered_suppliers = [supplier for supplier in all_suppliers if 
                          search_term in supplier['business_name'].lower() or 
                          search_term in supplier['contact'].lower() or
                          search_term in supplier['phone'].lower() or 
                          search_term in supplier['email'].lower() or
                          search_term in supplier['notes'].lower()
                          ]
  
    self.repeating_panel_suppliers.items = filtered_suppliers
    pass

  def reset_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.search_text_box.text = ""
    suppliers = supplier_cache.get_all_suppliers()
    self.repeating_panel_suppliers.items = suppliers
    pass
