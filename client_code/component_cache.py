import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

#======== GET COMPONENTS BY SUPPLIER

__supplier_components = []
def get_supplier_components(supplier_id):
  global __supplier_components 
  if __supplier_components:
    return __supplier_components
  else:
    __supplier_components = anvil.server.call('get_supplier_components', supplier_id)
    return __supplier_components

def refresh_supplier_components():
  global __supplier_components 
  __supplier_components = []
  return __supplier_components
  