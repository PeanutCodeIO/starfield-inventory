from ._anvil_designer import PO_FormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import main_functions_cache

class PO_Form(PO_FormTemplate):
  def __init__(self,company_id = None, supplier_id = None, po_id = None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.company_id = company_id
    self.supplier_id = supplier_id
    self.po_id = po_id

    # Any code you write here will run before the form opens.
    data = anvil.server.call('get_specific_po', supplier_id, po_id)

    company_name = main_functions_cache.get_company_name()
    self.company_name_label.text = company_name['company_name']
    

    po_number = data['purchase_order']['purchase_order_id']
    self.po_number_label.text = f"{po_number}"
    
    date = data['purchase_order']['purchase_order_date']
    self.date_label.text = date 

    status_list = [
    "Pending",
    "Emailed",
    "Invoiced",
    "Partial Payment",
    "Paid",
    "Shipped",
    "Received",  # Corrected spelling
    ]

    self.status_drop_down.items = status_list
    
    status = data['purchase_order']['status']
    if status in status_list:
        self.status_drop_down.selected_value = status
    else:
        # Handle the case where status is not in the list
        # For example, set to a default value or log an error
        self.status_drop_down.selected_value = None  # or your default value


    
    print(data['components'])

  def close_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Purchase_Orders', self.supplier_id)
    pass
    
