from ._anvil_designer import Component_ListTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import component_cache

class Component_List(Component_ListTemplate):
  def __init__(self,supplier_id = None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id

    # Any code you write here will run before the form opens.
    components = component_cache.get_supplier_components(supplier_id)
    self.component_repeating_panel.items = components

    self.repeating_panel_1.items = components
    

  def search_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    search_term = self.search_text_box.text.lower()
    all_components = component_cache.get_supplier_components(self.supplier_id)

    filtered_component = [
    component for component in all_components 
    if search_term in component['item_name'].lower() or
       search_term in str(component['sku']).lower() or
       search_term in str(component['item_cost']).lower() or 
       search_term in str(component['order_minimun']).lower() or
       search_term in str(component['low_stock_alert']).lower() or
       search_term in str(component['minimum_order_cost']).lower() or
       search_term in component['description'].lower()
      ]

    self.component_repeating_panel.items = filtered_component
    self.repeating_panel_1.items = filtered_component
    
    pass

  def reset_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.search_text_box.text = ""
    self.component_repeating_panel.items = component_cache.get_supplier_components(self.supplier_id)
    pass


    
