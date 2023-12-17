import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import io
import csv

#===== GET COMPANY ID
def get_company_id():
  user = anvil.users.get_user()
  return user['company_id']


#____ Auto Increment New Component 
def auto_increment_component_id():
    company_id = get_company_id()
  
    # Create a new component_id
    component_data = app_tables.components.search(company_id=company_id)
    if component_data:
        last_component_id = max((d['component_id'] for d in component_data if d['component_id'] is not None), default=0)
        next_component_id = last_component_id + 1
    else:
        next_component_id = 1

    return next_component_id


#____ Save a new component under a supplier

@anvil.server.callable
def save_new_component(component_data):

  company_id = get_company_id()
  component_id = auto_increment_component_id()
    
  # Replace empty fields with "No Data"
  for key in ['sku', 'description']:
      if not component_data.get(key):
          component_data[key] = "No Data"
  
  # Add a new row to the components table
  app_tables.components.add_row(
     company_id=company_id,
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
  company_id = get_company_id()
  components = app_tables.components.get(company_id=company_id ,supplier_id=supplier_id, component_id=component_data['component_id']).update(
    
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
  company_id = get_company_id()
  return app_tables.components.search(company_id=company_id,supplier_id=supplier_id)



#======== CREATE IMPORT TEMPLATE

@anvil.server.callable
def create_component_import_template(supplier_id):
  company_id = get_company_id()
  headers = ["Component", "Part Number", "Description", "Cost", "Unit Measurement", "Order Minimum", "Low Stock Alert"]
  supplier_name = app_tables.suppliers.get(company_id=company_id,supplier_id=supplier_id)
  business_name = supplier_name['business_name']


  
  # Use StringIO to create a file-like object in memory
  output = io.StringIO()
  writer = csv.writer(output)
  writer.writerow(headers)

  # Convert the StringIO object to a Media object
  return anvil.BlobMedia('text/csv', output.getvalue().encode(), name=f'{business_name}.csv')



#======== UPLOAD AND UPDATE COMPONENTS
@anvil.server.callable
def upload_csv_and_create_components(file, supplier_id):
    company_id = get_company_id()
    # Read the uploaded CSV file
    file_content = file.get_bytes().decode('utf-8')
    file_io = io.StringIO(file_content)
    reader = csv.reader(file_io)
    
    # Get the headers from the first row of the CSV
    headers = next(reader)
    
    supplier_link = app_tables.suppliers.get(company_id=company_id,supplier_id=supplier_id)

    # Create a dictionary to map the CSV headers to the database column names
    header_map = {
        "Component": "item_name", 
        "Part Number": "sku", 
        "Description": "description", 
        "Cost": "item_cost",  # number
        "Unit Measurement": "unit_measurement", 
        "Order Minimum": "order_minimun",  # number
        "Low Stock Alert": "low_stock_alert",  # number
    }

    for row in reader:
        component_data = {header_map[header]: value for header, value in zip(headers, row)}
        component_data['supplier_id'] = supplier_id  # Add the supplier link directly

        # Convert the fields expected to be numbers
        number_fields = ['item_cost', 'order_minimun', 'low_stock_alert']
        for field in number_fields:
            try:
                component_data[field] = float(component_data.get(field, 0))
            except ValueError:
                component_data[field] = 0.0  # default value if conversion fails
        
        # Calculate minimum_order_cost
        cost = component_data.get('item_cost', 0)
        order_minimun = component_data.get('order_minimun', 1)
        component_data['minimum_order_cost'] = cost * order_minimun if order_minimun else 0

        # Check if a component with the given name already exists
        existing_component = app_tables.components.get(company_id=company_id,sku=component_data['sku'])
        
        # Add or update the component data in the table
        if existing_component:
            existing_component.update(**component_data)
        else:
            component_data['component_id'] = auto_increment_component_id()  # Ensure this function exists
            app_tables.components.add_row(company_id=company_id, **component_data)

    return "Upload and component creation successful!"
