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
from .... import supplier_cache

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

    invoice_number = data['purchase_order']['invoice_number']
    invoice_amount = data['purchase_order']['invoice_total']
    invoice_owing = data['purchase_order']['invoice_owing']

    self.invoice_no_textbox.text = invoice_number
    self.invoice_amount_textbox.text = invoice_amount
    self.owing_textbox.text = invoice_owing

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

    components = data['components']
    self.po_repeating_panels.items = components
    
    print(data['components'])

  def close_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Purchase_Orders', self.supplier_id)
    pass

  def status_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""

    status_list = [
    "Pending",
    "Emailed",
    "Invoiced",
    "Partial Payment",
    "Paid",
    "Shipped",
    "Received",  # Corrected spelling
    ]

    status = self.status_drop_down.selected_value
    anvil.server.call('update_status', self.supplier_id, self.po_id, status)
    supplier_cache.refresh_purchase_orders()
    
    
    if status == "Invoiced":
      # Create a TextBox
      t = TextBox(placeholder="Invoice Number")
      a = TextBox(placeholder="Invoice Amount")
      o = TextBox(placeholder="Payments Made?", text="0")
      # Display the TextBox in an alert with a title
      invoice_number = anvil.alert(content=t, title="Enter Invoice Number", buttons=[("Save", True), ("Cancel", False)])

      if invoice_number:
        self.invoice_no_textbox.text = t.text

        invoice_amount = anvil.alert(content=a, title="Enter Invoice Amount", buttons=[("Save", True)])
        
        if invoice_amount:
          self.invoice_amount_textbox.text = a.text

          payment = anvil.alert(content=o, title="Payment Made?", buttons=[("Paid", True), ("Add Payment", False), ("None", None)])

          if payment:
            self.owing_textbox.text = "0"
            
            self.status_drop_down.items = status_list
            new_status = self.status_drop_down.selected_value = "Paid"
            
            anvil.server.call('update_invoice_details', self.supplier_id, self.po_id, new_status,self.invoice_no_textbox.text,
                                                        int(self.invoice_amount_textbox.text), self.owing_textbox.text)            
            supplier_cache.refresh_purchase_orders()
          elif payment == False:
            total = int(self.invoice_amount_textbox.text) - int(o.text)
            self.owing_textbox.text = total
            self.status_drop_down.items = status_list
            new_status = self.status_drop_down.selected_value = "Partial Payment"
            
            anvil.server.call('update_invoice_details', self.supplier_id, self.po_id, new_status,self.invoice_no_textbox.text,
                                                        int(self.invoice_amount_textbox.text), self.owing_textbox.text)
            
            
            supplier_cache.refresh_purchase_orders()
          elif payment == None:
            self.owing_textbox.text = int(self.invoice_amount_textbox.text)
            anvil.server.call('update_invoice_details', self.supplier_id, self.po_id, status,self.invoice_no_textbox.text,
                                                        int(self.invoice_amount_textbox.text), self.owing_textbox.text)
            supplier_cache.refresh_purchase_orders()
      else:
        return None

    pass

  def add_payment_button_click(self, **event_args):
    """This method is called when the button is clicked"""

    status_list = [
    "Pending",
    "Emailed",
    "Invoiced",
    "Partial Payment",
    "Paid",
    "Shipped",
    "Received",  # Corrected spelling
    ]

    
    t = TextBox(placeholder="Enter Amount")
    payment = anvil.alert(content=t, title="Add Payment", buttons=[("Full Amount", "Paid"),("Add", True), ("Cancel", False)])

    if payment == "Paid":
      amount = self.owing_textbox.text = "0"
      anvil.server.call('update_po_owing', self.supplier_id, self.po_id, amount)
      self.status_drop_down.items = status_list
      new_status = self.status_drop_down.selected_value = "Paid"
      anvil.server.call('update_status', self.supplier_id, self.po_id, new_status)
      
      supplier_cache.refresh_purchase_orders()
      
    elif payment == True:
      payment = int(t.text)
      total = int(self.owing_textbox.text) - payment
      self.owing_textbox.text = total
      
      anvil.server.call('update_po_owing', self.supplier_id, self.po_id, str(total))
      
      self.status_drop_down.items = status_list
      new_status = self.status_drop_down.selected_value = "Partial Payment"
      anvil.server.call('update_status', self.supplier_id, self.po_id, new_status)
      
      supplier_cache.refresh_purchase_orders()
      

    elif payment == False:
      return None
      
    
  
    pass
    
