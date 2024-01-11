from ._anvil_designer import Purchase_OrdersTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import supplier_cache

class Purchase_Orders(Purchase_OrdersTemplate):
  def __init__(self, supplier_id = None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id

    # Any code you write here will run before the form opens.
    purchase_orders = supplier_cache.get_purchase_orders(self.supplier_id)
    self.po_repeating_panel.items = purchase_orders
    

