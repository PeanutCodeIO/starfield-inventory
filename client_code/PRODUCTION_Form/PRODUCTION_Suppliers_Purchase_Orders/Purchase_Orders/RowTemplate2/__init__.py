from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.po_link.text = self.item['purchase_order_id']

  def form_link_click(self, **event_args):
    """This method is called when the link is clicked"""

    company_id = self.item['company_id']
    supplier_id = self.item['supplier_id']
    po_id = self.item['purchase_order_id']
    
    open_form("PRODUCTION_Form.PRODUCTION_Suppliers_Purchase_Orders.PO_Form", company_id, supplier_id, po_id)
    pass

  def po_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    company_id = self.item['company_id']
    supplier_id = self.item['supplier_id']
    po_id = self.item['purchase_order_id']
    
    open_form("PRODUCTION_Form.PRODUCTION_Suppliers_Purchase_Orders.PO_Form", company_id, supplier_id, po_id)
    
    pass

  

