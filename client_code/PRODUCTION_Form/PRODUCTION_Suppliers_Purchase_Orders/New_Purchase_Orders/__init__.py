from ._anvil_designer import New_Purchase_OrdersTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Add_Components import Add_Components
from .... import component_cache
from .... import supplier_cache

class New_Purchase_Orders(New_Purchase_OrdersTemplate):
  def __init__(self,supplier_id = None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id
    

    # Any code you write here will run before the form opens.
    supplier = supplier_cache.get_supplier_data(supplier_id)['business_name']
    print(supplier)
    self.supplier_label.text = supplier
    
    cmpt = Add_Components(self.supplier_id)
    self.content_panel.clear()
    self.content_panel.add_component(cmpt)
