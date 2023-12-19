from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate2(ItemTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.cmpt_label.text = self.item['item_name']
    self.sku_label.text = self.item['sku']
    self.cost_label.text = "{:.2f}".format(self.item['item_cost'])
    self.quantity_text_box.text = self.item['order_minimun']
    self.total_label.text = self.item['minimum_order_cost']

  def quantity_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""

    
    pass
    
