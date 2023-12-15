import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

#____ Auto Increment New Component 
def auto_increment_component_id():
    # Create a new component_id
    component_data = app_tables.components.search()
    if component_data:
        last_component_id = max((d['component_id'] for d in component_data if d['component_id'] is not None), default=0)
        next_component_id = last_component_id + 1
    else:
        next_component_id = 1

    return next_component_id


#____ Save a new component under a supplier

@anvil.server.callable
def save_new_component(component_data):
  
  component_id = auto_increment_component_id()
    
  # Replace empty fields with "No Data"
  for key in ['sku', 'description']:
      if not component_data.get(key):
          component_data[key] = "No Data"
  
  # Add a new row to the components table
  app_tables.components.add_row(
      component_id=component_id,
      supplier_id=component_data['supplier_id'],
      item_name=component_data['item_name'],
      sku=component_data['sku'],
      description=component_data['description'],
      item_cost=component_data['item_cost'],
      unit_measurement=component_data['unit_measurement'],
      order_minimun=component_data['order_minimum'],
      minimum_order_cost=component_data['minimum_order_cost'],
      low_stock_alert=component_data['low_stock_alert'],
  )
  
  return None
#____ EDIT COMPONENT UNDER A SUPPLIER

@anvil.server.callable
def edit_new_component(supplier_id, component_data):

  components = app_tables.components.get(supplier_id=supplier_id, component_id=component_data['component_id']).update(
    
      item_name=component_data['item_name'],
      sku=component_data['sku'],
      description=component_data['description'],
      item_cost=component_data['item_cost'],
      unit_measurement=component_data['unit_measurement'],
      order_minimun=component_data['order_minimum'],
      minimum_order_cost=component_data['minimum_order_cost'],
      low_stock_alert=component_data['low_stock_alert'],
  )
                                                                                                                     
  return None




#======== GET COMPONENTS BY SUPPLIER

@anvil.server.callable
def get_supplier_components(supplier_id):
  return app_tables.components.search(supplier_id=supplier_id)
  