from ._anvil_designer import New_CommodityTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class New_Commodity(New_CommodityTemplate):
  def __init__(self, supplier_id = None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id

    # Any code you write here will run before the form opens.
    measurements = [
    "Millimeters",
    "Centimeters",
    "Meters",
    "Milligrams",
    "Grams",
    "Kilograms",
    "Tonnes",
    "Milliliters",
    "Liters",
    "Cubic meters",
    "Square meters",
    "Pieces",
    "Units",
    "Packs",
    "Boxes",
    "Sheets",
    "Rolls",
    "Length"
    ]
    self.measurement_dd.items = measurements

  def close_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module.Suppliers_Commodities', self.supplier_id)
    pass

  def save_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    commodity = self.commodity_tb.text
    amount_text = self.quantity_tb.text
    measurement = self.measurement_dd.selected_value
    price_text = self.price_tb.text

    # Validate that all fields are filled
    if not (commodity and amount_text and measurement and price_text):
        anvil.alert("Please fill in all fields before saving.")
        return

    # Convert amount and price to their respective types
    try:
        amount = int(amount_text)
        price = float(price_text)
    except ValueError:
        anvil.alert("Invalid input in amount or price field.")
        return

    # Prepare the data
    data = {
        "supplier_id": self.supplier_id,
        "commodity_name": commodity,
        "commodity_amount": amount,
        "commodity_measurement": measurement,
        "commodity_price": price
    }

    # Confirm save operation
    message = anvil.alert(title="Do you wish to add another?", buttons=[("Add Another", True), ("Save & Exit", False)])
    if message:
        anvil.server.call('save_commodity', data)
        # Reset the fields for new input
        self.commodity_tb.text = ""
        self.quantity_tb.text = ""
        self.measurement_dd.selected_value = None
        self.price_tb.text = ""
    else:
        anvil.server.call('save_commodity', data)
        # Navigate to another form
        open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module.Suppliers_Commodities', self.supplier_id)



