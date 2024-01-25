from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.cmpt_id_label.text = self.item["sku"]
    self.cmpt_label.text = self.item["item_name"]
    self.cost_label.text = "{:.2f}".format(self.item['item_cost'])

    self.min_order_label.text = self.item["order_minimun"]
    self.stock_alert_label.text = self.item["low_stock_alert"]
    self.order_cost_label.text = self.item["minimum_order_cost"]

  def component_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    supplier_id = self.item['supplier_id']
    cmpt_id = self.item['component_id']
    switch = self.item['is_commodity']

    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module.Suppliers_Components.Edit_Component', supplier_id, cmpt_id, switch)
    pass


    
