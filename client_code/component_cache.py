import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

#===== CLEAR ALL CACHES FOR LOGOUT
def clear_all_caches():
  global __supplier_components
  __supplier_components = []
  

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

def get_component_data(supplier_id, cmpt_id):
  global __supplier_components

  if not __supplier_components:
    __supplier_components = anvil.server.call('get_supplier_components', supplier_id)

  for component in __supplier_components:
    if component['component_id'] == cmpt_id:
      return component
      
  return None



#-------------------- COMMODITIES ----------------------------------------------------------------------------------------

__supplier_commodities = []

def get_commodities(supplier_id):
  global __supplier_commodities
  if __supplier_commodities:
    return __supplier_commodities
  else:
    __supplier_commodities = anvil.server.call('get_commodities', supplier_id)
    
    return __supplier_commodities

def refresh_commodities():
  global __supplier_commodities
  __supplier_commodities = []
  return __supplier_commodities