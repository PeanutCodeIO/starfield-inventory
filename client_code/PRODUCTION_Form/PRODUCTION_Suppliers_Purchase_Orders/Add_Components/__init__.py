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
        order_minimum = row.item['order_minimun'] - 1 
        quantity_text = row.quantity_text_box.text

        # Skip rows with invalid or insufficient quantities
        if not quantity_text or int(quantity_text) <= order_minimum:
            continue

        # Process valid rows
        data = {
            "supplier_id": self.supplier_id, 
            "component_id": component_id,
            "quantity": float(quantity_text),
        }

        supplier_cache.recieve_po_components(data)
        added_count += 1 

    # Check if any products were added
    if added_count > 0:
      
       # supplier_cache.save_po_components()

        confirm = anvil.alert(title="Complete this purchase order?", buttons=[("Yes", True), ("No", False)])
        if confirm:
          supplier_cache.save_po_components()
          supplier_cache.refresh_po_data()
  
          email = anvil.alert(title="Email supplier this purchase order?", buttons=[("Yes", True), ("No", False)])
          if email:
            anvil.server.call('email_po_order', self.supplier_id)
            anvil.alert("Email sent, Purchase order complete")
            open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Purchase_Orders', self.supplier_id)
            return 
            
          else:
            open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Purchase_Orders', self.supplier_id)            
            return

        else:
          open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Purchase_Orders', self.supplier_id)
          return #if confirm is False
          
        #print(po_data)
        
        
    else:
        anvil.alert(title="No products selected or components are below minimum order",
                    message="Please enter quantities for products you want to add.")



  
