from ._anvil_designer import PRODUCTION_Suppliers_Purchase_OrdersTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Purchase_Orders import Purchase_Orders
from .New_Purchase_Orders import New_Purchase_Orders
from ... import supplier_cache

class PRODUCTION_Suppliers_Purchase_Orders(PRODUCTION_Suppliers_Purchase_OrdersTemplate):
  def __init__(self,supplier_id = None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id

    # Any code you write here will run before the form opens.
    supplier = supplier_cache.get_supplier_data(supplier_id)['business_name']
    self.supplier_label.text = supplier
    

  def new_po_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Purchase_Orders.New_Purchase_Orders', self.supplier_id)
    
    pass
