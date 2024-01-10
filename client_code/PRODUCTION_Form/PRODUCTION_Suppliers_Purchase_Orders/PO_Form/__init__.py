from ._anvil_designer import PO_FormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PO_Form(PO_FormTemplate):
  def __init__(self,company_id = None, supplier_id = None, po_id = None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.company_id = company_id
    self.supplier_id = supplier_id
    self.po_id = po_id

    # Any code you write here will run before the form opens.
