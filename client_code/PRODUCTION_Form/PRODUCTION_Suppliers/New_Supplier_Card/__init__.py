from ._anvil_designer import New_Supplier_CardTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import supplier_cache

class New_Supplier_Card(New_Supplier_CardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_close_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers')
    pass

  def button_save_click(self, **event_args):
    """This method is called when the button is clicked"""
    text_boxes = {
    'business_name': self.text_box_business_name,
    'address': self.text_area_address,
    'phone': self.text_box_phone,
    'email': self.text_box_email,
    'website': self.text_box_website,
    }
    
    optional_text_boxes = {
        'abn': self.text_box_abn,
        'contact': self.text_box_contact,
        'customer_ref': self.text_box_customer_ref,
        'payment_terms': self.text_box_payment_terms,
        'bank_name': self.text_box_bank_name,
        'bsb': self.text_box_bsb,
        'account': self.text_box_account,
        'fullfillment': self.text_box_fullfillment,
        'notes': self.text_area_notes
    }
    
    empty_fields = []
    
    for field_name, text_box in text_boxes.items():
        if text_box.text == "":
            empty_fields.append(field_name)
    
    if empty_fields:
        anvil.alert(f"Please enter all required fields: {', '.join(empty_fields)}")
    else:
        all_data = {k: v.text for k, v in {**text_boxes, **optional_text_boxes}.items()}
        anvil.server.call('save_new_supplier', all_data)
        anvil.alert("Supplier saved")
        # Clear all text boxes
        for text_box in {**text_boxes, **optional_text_boxes}.values():
            text_box.text = ""
        supplier_cache.refresh_all_suppliers()
        open_form("PRODUCTION_Form.PRODUCTION_Suppliers")
      
    pass
