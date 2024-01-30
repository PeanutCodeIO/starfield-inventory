import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from . import component_cache
from . import supplier_cache



#--------------------LOGOUT AND CLEAR ALL CACHES --------------------
def clear_all_caches():
  global __company_name
  __company_name = [] 
  component_cache.clear_all_caches() #Components Cache
  supplier_cache.clear_all_caches() #Suppliers Cache


#-------------------- GET COMPANY NAME #--------------------
__company_name = []
def get_company_name():
  global __company_name
  if not __company_name:
    __company_name = anvil.server.call('get_company_name')
    return __company_name
  else:
    return __company_name


#-------------------- GET UNITS #--------------------
__unit_list = []

def get_unit_list():
  global __unit_list
  if __unit_list:
    return __unit_list
  else:
    __unit_list = anvil.server.call('get_unit_list')

