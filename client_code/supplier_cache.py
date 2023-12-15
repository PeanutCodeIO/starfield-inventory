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


#___ Get a single supplier data
def get_supplier_data(supplier_id):
    global __all_suppliers

    # Ensure __all_suppliers is populated
    if not __all_suppliers:
        __all_suppliers = anvil.server.call('get_all_suppliers')

    # Search for the supplier with the given supplier_id
    for supplier in __all_suppliers:
        if supplier['supplier_id'] == supplier_id:
            return supplier

    # Return None if no matching supplier is found
    return None
