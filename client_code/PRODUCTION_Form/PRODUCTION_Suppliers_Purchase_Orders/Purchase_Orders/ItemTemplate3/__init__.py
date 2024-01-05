from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate3(ItemTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.date_label.text = self.item['purchase_order_date']
    self.po_number_label.text = self.item['purchase_order_id']
    self.status_label.text = self.item['status']
    self.invoice_number_label.text = self.item['invoice_number'] if self.item['invoice_number'] is not None else "Pending"
    self.invoice_amount_label.text = self.item['invoice_total'] if self.item['invoice_total'] is not None else "Pending"
    self.owing_label.text = self.item['invoice_owing'] if self.item['invoice_owing'] is not None else "Pending"

