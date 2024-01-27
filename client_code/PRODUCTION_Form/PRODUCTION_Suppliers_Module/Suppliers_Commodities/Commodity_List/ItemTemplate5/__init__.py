from ._anvil_designer import ItemTemplate5Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...... import component_cache

class ItemTemplate5(ItemTemplate5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.com_lbl.text = self.item["commodity_name"]
    self.price_lbl.text = self.item["commodity_price"]
    self.amount_lbl.text = self.item["commodity_amount"]
    self.measurement_lbl.text = self.item['commodity_measurement']
    self.updated_lbl.text = self.item["date_updated"]

  def price_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    t = TextBox(placeholder="Update Price")
    alert = anvil.alert(content=t, title="Update new price", buttons=[("Update", "Save"), ("Cancel", "Cancel")])
    if alert == "Save":
      self.price_lbl.text = float(t.text)
      
      supplier_id = self.item['supplier_id']
      commodity_id = self.item['commodity_id']
      
      new_price = float(self.price_lbl.text)

      anvil.server.call('update_commodity_price', supplier_id, commodity_id, new_price)
      component_cache.refresh_commodities()
      component_cache.refresh_supplier_components()
      return
    elif alert == "Cancel":
      return
    pass
    
