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
    self.quantity_text_box.text = "0"
    self.min_order_label.text = self.item['order_minimun']

    cost = float(self.item['item_cost'])
    quantity = float(self.quantity_text_box.text)

    self.total_label.text = cost*quantity


  def quantity_text_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    try:
        # Ensure text box values are treated as strings
        cost_text = str(self.item['item_cost'])
        quantity_text = str(self.quantity_text_box.text)

        # Use a default value of 0.0 if the text box is empty or contains non-numeric text
        cost = float(cost_text) if cost_text.strip() else 0.0
        quantity = float(quantity_text) if quantity_text.strip() else 0.0

        # Calculate and format the result to two decimal places
        calculated_cost = cost * quantity
        self.total_label.text = "{:.2f}".format(calculated_cost)

        # Update the total in the main form
        main_form = self.parent.parent.parent  # Adjust according to your form hierarchy
        main_form.calculate_total()
    except ValueError:
        # Handle cases where the input cannot be converted to a float
        self.total_label.text = "0.00"

    
    
