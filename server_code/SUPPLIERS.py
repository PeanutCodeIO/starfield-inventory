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

#===== GET COMPANY ID
def get_company_id():
  return anvil.users.get_user()['company_id']

#===== AUTO INCREMENT SUPPLIER IDS
def auto_increment_supplier_id():
    # Create a new supplier_id
    company_id = get_company_id()
    supplier_data = app_tables.suppliers.search(company_id=company_id)
    if supplier_data:
        last_supplier_id = max((d['supplier_id'] for d in supplier_data if d['supplier_id'] is not None), default=0)
        next_supplier_id = last_supplier_id + 1
    else:
        next_supplier_id = 1

    return next_supplier_id


#===== GET COMAPANYS SUPPLIERS
@anvil.server.callable
def get_all_suppliers():
  company_id = get_company_id()
  return app_tables.suppliers.search(company_id=company_id)


#____ Create a new supplier
@anvil.server.callable
def save_new_supplier(all_data):
    company_id = get_company_id()
    id = auto_increment_supplier_id()
    app_tables.suppliers.add_row(company_id=company_id, supplier_id=id, **all_data)

#____ Edit a supplier
@anvil.server.callable
def update_supplier_details(supplier_id, **data):
  company_id = get_company_id()
  supplier = app_tables.suppliers.get(company_id=company_id, supplier_id=supplier_id).update(**data)
  return None

#____ Export CSV File
@anvil.server.callable
def create_suppliers_import_template():
    # Define the headers for your CSV file
    headers = ["Business Name", "ABN", "Address", "Contact", "Phone", "Email", "Website","Customer Reference ID", "Payment Terms", "Bank Account Name", "BSB", "Account", "Fullfillment Time", "Notes" ]
  
    # Use StringIO to create a file-like object in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)

    # Convert the StringIO object to a Media object
    return anvil.BlobMedia('text/csv', output.getvalue().encode(), name='suppliers_template.csv')






@anvil.server.callable
def upload_csv_and_create_suppliers(file):
    company_id = get_company_id()
    # Read the uploaded CSV file
    file_content = file.get_bytes().decode('utf-8')
    file_io = io.StringIO(file_content)
    reader = csv.reader(file_io)
    
    # Get the headers from the first row of the CSV
    headers = next(reader)
    
    # Create a dictionary to map the CSV headers to the database column names
    header_map = {
        "Business Name": "business_name",
        "ABN": "abn",
        "Address": "address",
        "Contact": "contact",
        "Phone": "phone",
        "Email": "email",
        "Website": "website",
        "Customer Reference ID":"customer_ref",
        "Payment Terms": "payment_terms",
        "Bank Account Name": "bank_name",
        "BSB": "bsb",
        "Account": "account",
        "Fullfillment Time": "fullfillment",
        "Notes": "notes"
    }
    
    # Loop through each row in the CSV file
    for row in reader:
        supplier_data = {header_map[header]: value for header, value in zip(headers, row)}
        
        # Search for an existing supplier with the given business name
        existing_suppliers = app_tables.suppliers.search(company_id=company_id, business_name=supplier_data["business_name"])
        
        # Check if any suppliers were found
        existing_supplier = None
        for supplier in existing_suppliers:
            existing_supplier = supplier
            break
        
        if existing_supplier:
            # Update the existing supplier row
            for key, value in supplier_data.items():
                setattr(existing_supplier, key, value)
        else:
            # If no existing supplier, add a new row
            supplier_data["supplier_id"] = auto_increment_supplier_id()
            supplier_data['company_id'] = company_id
            app_tables.suppliers.add_row(**supplier_data)

    return "Upload and supplier creation successful!"


#===== COMPONENT PURCHASE ORDERS
def auto_increment_po_id():
    # Create a new po_id
    company_id = get_company_id()
    po_data = app_tables.purchase_orders.search(company_id=company_id)
    if po_data:
        last_supplier_id = max((d['purchase_order_id'] for d in po_data if d['purchase_order_id'] is not None), default=0)
        next_supplier_id = last_supplier_id + 1
    else:
        next_supplier_id = 1

    return next_supplier_id

@anvil.server.callable
def save_po_data(data):
  print(f"This is the saved data in {data}")
  company_id = get_company_id()
  supplier_id = data[0]['supplier_id'] 
  purchase_order_id = auto_increment_po_id() 
  purchase_order_date = datetime.now().date()
  status = "Pending"

  app_tables.purchase_orders.add_row(company_id=company_id, 
                                     supplier_id=supplier_id, 
                                     purchase_order_id=purchase_order_id,
                                     purchase_order_date=purchase_order_date,
                                     status=status)

  for item in data:
    component = item['component_id']
    quantity = item['quantity']
    app_tables.purchase_orders_components.add_row(company_id=company_id,
                                                  supplier_id=supplier_id,
                                                  purchase_order_id=purchase_order_id,
                                                  component_id=component,
                                                  quantity=quantity)

  
  
  
  return

@anvil.server.callable
def email_po_order(supplier_id):
    company_id = get_company_id()
    # Search for the last purchase order
    last_po_iter = app_tables.purchase_orders.search(
        tables.order_by("purchase_order_id", ascending=False),
        company_id=company_id,
        supplier_id=supplier_id,
    )

    # Get the first entry from the iterator, which is the last purchase order
    last_po_entry = next(iter(last_po_iter), None)
    
    if last_po_entry is None:
        # Handle case where there is no purchase order
        print("No purchase order found.")
        return

    purchase_order = app_tables.purchase_orders.get(company_id=company_id,
                                                  supplier_id=supplier_id,
                                                  purchase_order_id=last_po_entry['purchase_order_id'])

    # Get the components associated with the last purchase order
    components = app_tables.purchase_orders_components.search(
        company_id=company_id, 
        supplier_id=supplier_id,
        purchase_order_id=last_po_entry['purchase_order_id']
    )

    # Prepare the data to be emailed
    purchase_order_data = {
        "purchase_order": purchase_order,
        "components": components
    }

    #Call the function to create a PDF

      
    # Call the function to email the supplier
    email =  email_supplier(purchase_order_data)
    app_tables.purchase_orders.get(company_id=company_id, supplier_id=supplier_id, purchase_order_id=last_po_entry['purchase_order_id']).update(status=email)
    return 

def email_supplier(purchase_order_data):
    purchase_order = purchase_order_data['purchase_order']
    components = purchase_order_data['components']

    company_id = get_company_id()
    company = app_tables.company.get(company_id=company_id)
    company_name = company['company_name']
  
    supplier_id = purchase_order['supplier_id']
    supplier = app_tables.suppliers.get(company_id=company_id, supplier_id=supplier_id)
    supplier_email = supplier['email'] if supplier else 'default@example.com'
    customer_id = supplier['customer_ref']

    # Construct the components details string
    components_details = ""
    for component_entry in components:
        component_id = component_entry['component_id']
        quantity = component_entry['quantity']

        # Fetch component details from the components table
        component = app_tables.components.get(company_id=company_id,component_id=component_id)
        if component:
            component_name = component['item_name']
            sku = component['sku']
            components_details += f"\nName: {component_name}\nSKU: {sku}\nQuantity: {quantity}\n"

    # Construct the email body
    email_body = (
        f"Hi, We would like to place a new purchase order for {company_name}, {customer_id}."
        "Please find the order details below:\n" + 
        components_details +
        "\nThank you."
    )

    
    # Send the email
    anvil.email.send(
        from_name=company_name,
        to=supplier_email,
        subject=f"New Purchase Order {customer_id}",
        text=email_body,
        # Attachments can be included if needed
        # attachments=[anvil.BlobMedia("application/pdf", pdf_bytes, name="PurchaseOrder.pdf")]
    )
    status = "Emailed"
    return status

def create_po_pdf():
  return

@anvil.server.background_task
def create_po_pdf_background():
  return

#-------------------- GET PURCHASE ORDERS ----------------------

@anvil.server.callable
def get_purchase_orders(supplier):
  company_id = get_company_id()
  supplier_id = supplier
    
  return app_tables.purchase_orders.search(company_id=company_id, supplier_id=supplier_id)

@anvil.server.callable
def get_specific_po(supplier_id, po_id):
  
  company_id = get_company_id()
  po_order = app_tables.purchase_orders.get(company_id=company_id, supplier_id=supplier_id, purchase_order_id=po_id)
  po_components = app_tables.purchase_orders_components.search(company_id=company_id,
                                                                supplier_id=supplier_id,
                                                                purchase_order_id=po_id)

  # Prepare the data to be emailed
  purchase_order_data = {
      "purchase_order": po_order,
      "components": po_components
  }
  
  
  return purchase_order_data