from ._anvil_designer import PRODUCTION_Suppliers_ModuleTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PRODUCTION_Suppliers_Module(PRODUCTION_Suppliers_ModuleTemplate):
  def __init__(self, supplier_id =None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id
    print(supplier_id)

    # Any code you write here will run before the form opens.
