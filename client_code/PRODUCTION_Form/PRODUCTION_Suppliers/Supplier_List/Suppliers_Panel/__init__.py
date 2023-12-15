from ._anvil_designer import Suppliers_PanelTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Suppliers_Panel(Suppliers_PanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.business_name_label.text = self.item['business_name']
    self.contact_label.text = self.item['contact']
    self.phone_label.text = self.item['phone']
    self.email_label.text = self.item['email']
    

  def supplier_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    supplier_id = self.item['supplier_id']
    supplier_name = self.item['business_name']
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module', supplier_id, supplier_name)
    pass
