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
from datetime import datetime

#-------------------- GET COMPANY ID ----------------------

def get_company_id():
  user = anvil.users.get_user()
  return user['company_id']

#-------------------- GET UNITS #--------------------

@anvil.server.callable
def get_unit_list():
  return app_tables.system_units.search()


#-------------------- Auto Increment New Component  ----------------------

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


#-------------------- Save a new component under a supplier #--------------------

@anvil.server.callable
def save_component_commodity(switch, data):
  if switch == True:
    save_new_comm_cmpt(data, switch)
    print(f"This is with comm {data}")
  else:
    save_new_component(data, switch)
    print(f"This is with comm {data}")
  return

def save_new_comm_cmpt(component_data, switch):

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
      commodity_measurement=component_data['commodity_measurement'],
      order_minimun=component_data['order_minimum'],
      minimum_order_cost=component_data['minimum_order_cost'],
      low_stock_alert=component_data['low_stock_alert'],
      commodity_id=component_data['commodity_id'],
      commodity_name=component_data['commodity_name'],
      commodity_amount=component_data['commodity_amount'],
      commodity_price=component_data['commodity_price'],
      is_commodity=switch,
  )

  current_date = datetime.now().date()
  component_cost = app_tables.components_cost_history.add_row(company_id=company_id, supplier_id=component_data['supplier_id'], component_id=component_id, item_cost=component_data['item_cost'], date=current_date)
  
  return None
  
@anvil.server.callable
def save_new_component(component_data, switch):

  company_id = get_company_id()
  component_id = auto_increment_component_id()
    
  # Replace empty fields with "No Data"
  for key in ['sku', 'description']:
      if not component_data.get(key):
          component_data[key] = "No Data"

  meaurement = app_tables.system_units.get(unit_id=component_data['unit_measurement_id'])
  unit_name = meaurement['unit']
  
  
  # Add a new row to the components table
  app_tables.components.add_row(
     company_id=company_id,
      component_id=component_id,
      supplier_id=component_data['supplier_id'],
      item_name=component_data['item_name'],
      sku=component_data['sku'],
      description=component_data['description'],
      item_cost=component_data['item_cost'],
      unit_measurement=unit_name,
      unit_measurement_id=meaurement,
      order_minimun=component_data['order_minimum'],
      minimum_order_cost=component_data['minimum_order_cost'],
      low_stock_alert=component_data['low_stock_alert'],
      is_commodity=switch,
  )

  current_date = datetime.now().date()
  component_cost = app_tables.components_cost_history.add_row(company_id=company_id, supplier_id=component_data['supplier_id'], component_id=component_id, item_cost=component_data['item_cost'], date=current_date)
  
  return None


#-------------------- EDIT COMPONENT UNDER A SUPPLIER  ----------------------
@anvil.server.callable
def edit_component_commodity(supplier_id, component_id, switch):

  if switch != True:
    edit_new_component(supplier_id, component_id)
  else:
    edit_component_commodity_task(supplier_id, component_id)
    return
  return


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

def edit_component_commodity_task(supplier_id, component_data):
  company_id = get_company_id()
  components = app_tables.components.get(company_id=company_id ,supplier_id=supplier_id, component_id=component_data['component_id']).update(
    
      item_name=component_data['item_name'],
      sku=component_data['sku'],
      description=component_data['description'],
      item_cost=component_data['item_cost'],
      unit_measurement=component_data['unit_measurement'],
      commodity_measurement=component_data['commodity_measurement'],
      order_minimun=component_data['order_minimum'],
      minimum_order_cost=component_data['minimum_order_cost'],
      low_stock_alert=component_data['low_stock_alert'],
      commodity_id=component_data['commodity_id'],
      commodity_name=component_data['commodity_name'],
      commodity_amount=component_data['commodity_amount'],
      commodity_price=component_data['commodity_price'],
    
  )
  
  return

#===== RECORD A COMPONENT PRICE CHANGE
@anvil.server.callable
def record_cmpt_cost_change(supplier_id, cmpt_id, new_cost):
  company_id = get_company_id()
  current_date = datetime.now().date()
  cmpt = app_tables.components_cost_history.add_row(company_id=company_id,
                                                   supplier_id=supplier_id,
                                                   component_id=cmpt_id,
                                                   date=current_date,
                                                   item_cost=new_cost)

  get_cmpt = app_tables.components.get(company_id=company_id,
                                               supplier_id=supplier_id,
                                               component_id=cmpt_id,
                                           )
  min_order = get_cmpt['order_minimun']
  new_min_cost = new_cost*min_order 

  update_main_cost = app_tables.components.get(company_id=company_id,
                                               supplier_id=supplier_id,
                                               component_id=cmpt_id).update(item_cost=new_cost, minimum_order_cost=new_min_cost)
  
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



@anvil.server.callable
def upload_csv_and_create_components(file, supplier_id):
    company_id = get_company_id()  # Function to retrieve the company ID
    current_date = datetime.now().date()  # Current date for cost history record

    # Read the uploaded CSV file
    file_content = file.get_bytes().decode('utf-8')
    file_io = io.StringIO(file_content)
    reader = csv.reader(file_io)
    
    # Get the headers from the first row of the CSV
    headers = next(reader)
    
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

        # Check if a component with the given SKU already exists
        existing_component = app_tables.components.get(company_id=company_id, sku=component_data['sku'])
        
        if existing_component:
            existing_component.update(**component_data)
            component_id = existing_component['component_id']  # Assuming component_id is stored in existing component
        else:
            component_id = auto_increment_component_id()  # Generate new component ID
            app_tables.components.add_row(company_id=company_id, component_id=component_id, **component_data)

        # Add a new row to the components_cost_history table
        app_tables.components_cost_history.add_row(
            company_id=company_id,
            supplier_id=supplier_id,
            component_id=component_id,
            item_cost=component_data['item_cost'],
            date=current_date
        )

    return "Upload and component creation successful!"




#-------------------- COMMODITIES ----------------------------------------------------------------------------------------




#-------------------- Auto Increment New Commodity  ----------------------
def auto_increment_commodity_id():
    company_id = get_company_id()
  
    # Create a new commodity_id
    commodity_data = app_tables.commodity.search(company_id=company_id)
    if commodity_data:
        last_commodity_id = max((d['commodity_id'] for d in commodity_data if d['commodity_id'] is not None), default=0)
        next_commodity_id = last_commodity_id + 1
    else:
        next_commodity_id = 1

    return next_commodity_id


@anvil.server.callable
def save_commodity(data):
  company_id = get_company_id()
  commodity_id = auto_increment_commodity_id()
  date = datetime.now().date()

  data['company_id'] = company_id
  data['commodity_id'] = commodity_id
  data['date_updated'] = date

  measurement = app_tables.system_units.get(unit_id=data['commodity_measurement_id'])
  unit_name = measurement['unit']

  data['commodity_measurement'] = unit_name

  app_tables.commodity.add_row(**data)
  return

@anvil.server.callable
def get_commodities(supplier_id):
  company_id = get_company_id()
  commodities = app_tables.commodity.search(company_id=company_id, supplier_id=supplier_id)
  return commodities



#-------------------- Update Commodity Price  ----------------------
@anvil.server.callable
def update_commodity_price(supplier_id, comm_id, price):
  company_id = get_company_id()
  date = datetime.now().date()
  app_tables.commodity.get(company_id=company_id, supplier_id=supplier_id,commodity_id=comm_id).update(commodity_price=price, date_updated=date)
  update_all_commodity_prices(company_id, supplier_id, comm_id)
  
  
  return

def update_all_commodity_prices(company_id, supplier_id, comm_id):
  component = app_tables.components.search(company_id=company_id, supplier_id=supplier_id, commodity_id=comm_id)
  
  commodity = app_tables.commodity.get(company_id=company_id, supplier_id=supplier_id, commodity_id=comm_id)
  comm_price = commodity['commodity_price']
  
  for comm in component:
    comm_amount = comm['commodity_amount']
    new_comm_price = comm_price * comm_amount
    minimum_order = comm['order_minimun']
    new_order_price = minimum_order * new_comm_price
    

    
    comm.update(commodity_price=new_comm_price, item_cost=new_comm_price, minimum_order_cost=new_order_price)
    
  return

