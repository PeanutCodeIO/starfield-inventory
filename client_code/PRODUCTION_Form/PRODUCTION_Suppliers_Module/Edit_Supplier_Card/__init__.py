from ._anvil_designer import Edit_Supplier_CardTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import supplier_cache
class Edit_Supplier_Card(Edit_Supplier_CardTemplate):
  def __init__(self, supplier_id = None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id
    
    # Any code you write here will run before the form opens.

    supplier_data = supplier_cache.get_supplier_data(supplier_id)

    # Set the text for each textbox, with a check for None values
    self.text_box_business_name.text = supplier_data['business_name'] if supplier_data['business_name'] is not None else "No Data"
    self.text_box_abn.text = supplier_data['abn'] if supplier_data['abn'] is not None else "No Data"
    self.text_area_address.text = supplier_data['address'] if supplier_data['address'] is not None else "No Data"
    self.text_box_phone.text = supplier_data['phone'] if supplier_data['phone'] is not None else "No Data"
    self.text_box_email.text = supplier_data['email'] if supplier_data['email'] is not None else "No Data"
    self.text_box_website.text = supplier_data['website'] if supplier_data['website'] is not None else "No Data"
    self.text_box_contact.text = supplier_data['contact'] if supplier_data['contact'] is not None else "No Data"
    self.text_box_customer_ref.text = supplier_data['customer_ref'] if supplier_data['customer_ref'] is not None else "No Data"
    self.text_box_payment_terms.text = supplier_data['payment_terms'] if supplier_data['payment_terms'] is not None else "No Data"
    self.text_box_bank_name.text = supplier_data['bank_name'] if supplier_data['bank_name'] is not None else "No Data"
    self.text_box_bsb.text = supplier_data['bsb'] if supplier_data['bsb'] is not None else "No Data"
    self.text_box_account.text = supplier_data['account'] if supplier_data['account'] is not None else "No Data"
    self.text_box_fullfillment.text = supplier_data['fullfillment'] if supplier_data['fullfillment'] is not None else "No Data"
    self.text_area_notes.text = supplier_data['notes'] if supplier_data['notes'] is not None else "No Data"


    
    
    

  

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
      anvil.server.call('update_supplier_details', self.supplier_id, **all_data)
      anvil.alert("Supplier updated")
      # Clear all text boxes
     # for text_box in {**text_boxes, **optional_text_boxes}.values():
        #text_box.text = ""
      supplier_cache.refresh_all_suppliers()
      
    pass
