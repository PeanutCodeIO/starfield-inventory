from ._anvil_designer import ItemTemplate4Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate4(ItemTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.cmpt_label.text = self.item['item_name']
    self.cmpt_sku.text = self.item['sku']
    component = self.quantity_label.text = self.item['quantity']
    measurement = self.measurement_label.text = self.item['unit_measurement']
    
