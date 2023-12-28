from ._anvil_designer import Add_ComponentsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import component_cache
from .... import supplier_cache

class Add_Components(Add_ComponentsTemplate):
  def __init__(self,supplier_id = None,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id
    
    # Any code you write here will run before the form opens.
    components = component_cache.get_supplier_components(self.supplier_id)
    self.cmpt_repeating_panel.items = components

  def search_text_box(self, **event_args):
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

    self.cmpt_repeating_panel.items = filtered_component

    
    pass

  def reset_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.search_text_box.text = ""
    components = component_cache.get_supplier_components(self.supplier_id)
    self.cmpt_repeating_panel.items = components
    pass


  def calculate_total(self):
    total = 0 
    for row in self.cmpt_repeating_panel.get_components():
      total += float(row.total_label.text)
    self.est_total_label.text = "{:.2f}".format(total)
    self.total_lb.visible = True
    self.est_total_label.visible = True
    
    return


  
  def load_order_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    # Count how many products were added
    added_count = 0

    # Iterate over each row in the Repeating Panel
    for row in self.cmpt_repeating_panel.get_components():
      component_id = row.item['component_id']
      order_minimum = row.item['order_minimun'] -1 
      quantity = float(row.quantity_text_box.text)
      

      # Check if quantity is provided and is greater than minimum order
      if not row.quantity_text_box.text or int(row.quantity_text_box.text) <= order_minimum:
        continue  # Skip this product and move to the next one

      data = {
        "supplier_id": self.supplier_id, 
        "component_id": component_id,
        "quantity":quantity,
      }
  
      print(data)
      added_count += 1 
      
      # Only proceed if there are products to add
      if added_count > 0:
          supplier_cache.recieve_po_components(data)
        
          anvil.alert(title="Components Loaded")
  
          # Clear the quantity fields and perform other post-addition tasks
          for row in self.cmpt_repeating_panel.get_components():
              row.quantity_text_box.text = order_minimum
  
      
          #new_order_navigation.home_form.products_added_to_cart()
          #order_cache.refresh_finished_order()
    else:
        anvil.alert(title="No products selected or components are below minimum order", message="Please enter quantities for products you want to add.")
    
    pass


  
