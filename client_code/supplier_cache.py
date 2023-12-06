import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


# ____ Get all suppliers
__all_suppliers = [] 
def get_all_suppliers():
  global __all_suppliers
  if __all_suppliers:
    return __all_suppliers
  else:
    __all_suppliers = anvil.server.call('get_all_suppliers')
    return __all_suppliers

# ____ Refresh supplier list 
def refresh_all_suppliers():
  global __all_suppliers
  __all_suppliers = []
  return __all_suppliers
