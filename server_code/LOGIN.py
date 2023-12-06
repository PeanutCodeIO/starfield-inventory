import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

#____ Check if the user has entered name fields
@anvil.server.callable
def is_name_filled():
  user = anvil.users.get_user()
  name_filled = user['name_filled']
  return name_filled 

#____ Save users details
@anvil.server.callable
def new_user(first_name, last_name):
  user = anvil.users.get_user()
  user_id = auto_increment_user_id()
  email = user['email']
  app_tables.users.get(email=email).update(first_name=first_name, last_name=last_name, user_id=user_id, name_filled=True)
  return

#____ Auto Increment User Id
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


