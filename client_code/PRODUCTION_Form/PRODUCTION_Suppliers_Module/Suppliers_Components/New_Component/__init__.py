from ._anvil_designer import New_ComponentTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import component_cache

class New_Component(New_ComponentTemplate):
  def __init__(self,supplier_id = None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id

    # Any code you write here will run before the form opens.

    self.text_box_stock_alert.text = "0"
    self.text_box_item_cost.text = "0"
    self.text_box_order_minimum.text = "0"
    self.minimum_order_cost.text = "0"

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
    self.drop_down_primary_unit.items = measurements

  def close_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module.Suppliers_Components', self.supplier_id)
    pass

  def text_box_item_cost_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    try:
        # Ensure text box values are treated as strings
        cost_text = str(self.text_box_item_cost.text)
        minimum_order_text = str(self.text_box_order_minimum.text)

        # Use a default value of 0.0 if the text box is empty or contains non-numeric text
        cost = float(cost_text) if cost_text.strip() else 0.0
        minimum_order = float(minimum_order_text) if minimum_order_text.strip() else 0.0

        # Calculate and format the result to two decimal places
        calculated_cost = cost * minimum_order
        self.minimum_order_cost.text = "{:.2f}".format(calculated_cost)
    except ValueError:
        # Handle cases where the input cannot be converted to a float
        self.minimum_order_cost.text = ""
    except ZeroDivisionError:
        # Handle division by zero error
        self.minimum_order_cost.text = "Infinity"  # Or any other appropriate message


  def text_box_order_minimum_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    try:
        # Ensure text box values are treated as strings
        cost_text = str(self.text_box_item_cost.text)
        minimum_order_text = str(self.text_box_order_minimum.text)

        # Use a default value of 0.0 if the text box is empty or contains non-numeric text
        cost = float(cost_text) if cost_text.strip() else 0.0
        minimum_order = float(minimum_order_text) if minimum_order_text.strip() else 0.0

        # Calculate and format the result to two decimal places
        calculated_cost = cost * minimum_order
        self.minimum_order_cost.text = "{:.2f}".format(calculated_cost)
    except ValueError:
        # Handle cases where the input cannot be converted to a float
        self.minimum_order_cost.text = ""
    except ZeroDivisionError:
        # Handle division by zero error
        self.minimum_order_cost.text = "Infinity"  # Or any other appropriate message




  def button_save_click(self, **event_args):
    """This method is called when the button is clicked"""

    # Create a dictionary with all the new fields
    component_data = {
        "supplier_id": self.supplier_id,
        "item_name": self.text_box_component.text,
        "sku": self.text_box_sku.text,
        "description": self.text_area_description.text,
        "unit_measurement": self.drop_down_primary_unit.selected_value,
        "order_minimum": float(self.text_box_order_minimum.text) if self.text_box_order_minimum.text else 0.0,
        "item_cost": float(self.text_box_item_cost.text) if self.text_box_item_cost.text else 0.0,
        "minimum_order_cost": float(self.minimum_order_cost.text) if self.minimum_order_cost.text else 0.0 ,
        "low_stock_alert": float(self.text_box_stock_alert.text) if self.text_box_stock_alert.text else 0.0,
    }

    # Check if the mandatory fields are filled
    mandatory_fields = ["item_name", "description", "unit_measurement"]

    for field in mandatory_fields:
        if not component_data[field]:
            anvil.alert(f"Please fill out the {field.replace('_', ' ')} field.")
            return

    # Send the component data to the server for storage
    anvil.server.call('save_new_component', component_data)
    anvil.alert("Component data stored successfully.")

    # Refresh component data cache (if applicable)
    component_cache.refresh_supplier_components()

    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module.Suppliers_Components', self.supplier_id)
    pass

  def yes_radio_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    self.component_card.visible = False
    self.commodity_card.visible = True
    commodities = component_cache.get_commodities(self.supplier_id)
    commodity_items = []
    
    for commodity in commodities:
        commodity_name = commodity['commodity_name']
        commodity_items.append((commodity_name, commodity_name))
    
    self.commodity_dd.items = commodity_items

    pass

  def no_radio_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    self.commodity_card.visible = False
    self.component_card.visible = True
    pass

  

