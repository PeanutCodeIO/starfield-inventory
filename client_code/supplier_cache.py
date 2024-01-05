import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

#-------------------- CLEAR ALL CACHES FOR LOGOUT ----------------------
def clear_all_caches():
  global __all_suppliers
  __all_suppliers = []


#-------------------- SUPPLIER DATA ----------------------

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


#-------------------- PURCHASE ORDERS ----------------------
__po_components = []

def recieve_po_components(data):
    global __po_components
    __po_components.append(data)  # Append the new entry to the list
    #print(f"This is in the cache: {__po_components}")

def get_po_components():
  global __po_components
  return __po_components

def save_po_components():
  global __po_components
  anvil.server.call('save_po_data', __po_components)
  return

def refresh_po_data():
  global __po_components
  __po_components = [] 


#-------------------- GET PURCHASE ORDERS ----------------------

__purchase_orders = []
def get_purchase_orders(supplier_id):
  global __purchase_orders
  if __purchase_orders:
    return __purchase_orders
  else:
    __purchase_orders = anvil.server.call('get_purchase_orders', supplier_id)
  return __purchase_orders

def refresh_purchase_orders():
  global __purchase_orders
  __purchase_orders = []
  return __purchase_orders