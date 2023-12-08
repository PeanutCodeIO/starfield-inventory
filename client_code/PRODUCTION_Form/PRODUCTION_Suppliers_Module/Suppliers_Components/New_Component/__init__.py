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
        cost = float(self.text_box_item_cost.text)
        minimum_order = float(self.text_box_order_minimum.text)
        self.minimum_order_cost.text = str(cost * minimum_order)
    except ValueError:
        # Handle cases where the input cannot be converted to a float
        self.minimum_order_cost.text = ""
        pass
    except ZeroDivisionError:
        # Handle division by zero error
        pass

  def text_box_order_minimum_change(self, **event_args):
      """This method is called when the text in this text box is edited"""
      try:
          cost = float(self.text_box_item_cost.text)
          minimum_order = float(self.text_box_order_minimum.text)
          self.minimum_order_cost.text = str(cost * minimum_order)
      except ValueError:
          # Handle cases where the input cannot be converted to a float
          self.minimum_order_cost.text = ""
          pass
      except ZeroDivisionError:
          # Handle division by zero error
          pass


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
    component_cache.refresh_supplier_components(self.supplier_id)

    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module.Suppliers_Components', self.supplier_id)
    pass

  def text_box_item_cost_change(self, **event_args):
    """This method is called when the text in this text box is edited"""

    
    pass

  

