import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import random 



#===== AUTO INCREMENT NEW USER
@anvil.server.callable
def auto_increment_user_id():
    user = anvil.users.get_user()
    user_id = user['user_id']

    if user_id is None:
        users = app_tables.users.search()
        if users:
            last_id = max([d['user_id'] or 0 for d in users])
            next_id = last_id + 1
        else:
            next_id = 1
        user.update(user_id=next_id)
        return next_id
    else:
        return user_id



#===== GENERATE COMPANY NAME AND USER ADMIN
@anvil.server.callable
def new_company(company_name, first_name, last_name):
    
  company_id = generate_unique_pin()

  user = anvil.users.get_user()
  
  user_id = auto_increment_user_id()
  email = user['email']

  app_tables.users.get(email=email).update(company_id=company_id,first_name=first_name, last_name=last_name, user_id=user_id, name_filled=True, is_admin=True)
  app_tables.company.add_row(company_id=company_id, company_name=company_name)
  
  return company_id  # Return the unique company_id

# Function to generate a unique PIN
def generate_unique_pin():
    while True:
        company_id = float(generate_pin()) 
        existing_company = app_tables.company.get(company_id=company_id)
        if not existing_company:
            return company_id

def generate_pin():
    # Generate a 6-digit PIN
    return "{:06d}".format(random.randint(0, 999999))




#____ Check if the user has entered name fields
@anvil.server.callable
def is_name_filled():
    user = anvil.users.get_user()
    if user is not None:
        try:
            name_filled = user['name_filled']
            return name_filled if name_filled is not None else False
        except KeyError:
            # 'name_filled' key does not exist in the user dictionary
            return False
    else:
        # No user is logged in
        return False

@anvil.server.callable
def get_company_name():
  company_id = anvil.users.get_user()['company_id']
  company = app_tables.company.get(company_id=company_id)
  return company







