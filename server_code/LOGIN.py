import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import random 


#===== AUTO INCREMENT USERS
@anvil.server.callable
def auto_increment_user_id():
    try:
        user = anvil.users.get_user()
        if not user:
            raise ValueError("No user is currently logged in.")

        user_id = user.get('user_id')

        if user_id is None:
            try:
                # Assuming user_id is always an integer or None
                users = app_tables.users.search(tables.order_by("user_id", ascending=False), tables.limit(1))
                last_user = next(users, None)

                next_id = 1 if last_user is None else (last_user['user_id'] or 0) + 1
                user.update(user_id=next_id)
                return next_id
            except Exception as e:
                # Log the exception or handle it as per your application's requirements
                anvil.server.error(f"Error in fetching or updating user data: {e}")
                raise
        else:
            if not isinstance(user_id, int):
                raise TypeError("user_id is not an integer")
            return user_id

    except Exception as e:
        # Handle unexpected exceptions
        anvil.server.error(f"Unexpected error: {e}")
        raise


@anvil.server.callable
def new_company(company_name, first_name, last_name):
    """
    Create a new company entry and update the user's details with company information.

    Args:
    company_name (str): The name of the new company.
    first_name (str): The first name of the user.
    last_name (str): The last name of the user.

    Returns:
    int: The unique company ID generated for the new company.
    """
    # Ensure the user is logged in before proceeding
    user = anvil.users.get_user()
    if not user:
        raise ValueError("No user is currently logged in.")

    # Generate a unique company ID
    company_id = generate_unique_pin()

    # Auto increment the user ID
    user_id = auto_increment_user_id()

    # Retrieve the user's email
    email = user['email']

    # Update the user's record with the new company information
    user_row = app_tables.users.get(email=email)
    if user_row:
        user_row.update(
            company_id=company_id,
            first_name=first_name,
            last_name=last_name,
            user_id=user_id,
            name_filled=True,
            is_admin=True
        )
    else:
        raise ValueError("User record not found.")

    # Add the new company to the company table
    app_tables.company.add_row(company_id=company_id, company_name=company_name)

    # Return the unique company ID
    return company_id  

def generate_unique_pin():
    """
    Generate a unique PIN for the company ID.

    Returns:
    float: A unique company ID.
    """
    while True:
        company_id = float(generate_pin())
        # Check if the generated ID is already in use
        if not app_tables.company.get(company_id=company_id):
            return company_id

def generate_pin():
    """
    Generate a 6-digit PIN.

    Returns:
    str: A 6-digit PIN as a string.
    """
    # Randomly generate a 6-digit number and format it as a string
    return "{:06d}".format(random.randint(0, 999999))





@anvil.server.callable
def is_name_filled():
    """
    Check if the logged-in user has filled in their name fields.

    Returns:
    bool: True if the name fields are filled, False otherwise.
    """
    # Retrieve the currently logged-in user
    user = anvil.users.get_user()

    # Proceed only if there is a logged-in user
    if user is not None:
        try:
            # Attempt to retrieve the 'name_filled' attribute
            name_filled = user['name_filled']
            # Return the value of 'name_filled', or False if it is None
            return name_filled if name_filled is not None else False
        except KeyError:
            # The 'name_filled' attribute does not exist in the user record
            return False
    else:
        # Return False if no user is logged in
        return False


@anvil.server.callable
def get_company_name():
    """
    Retrieve the company name associated with the logged-in user's company ID.

    Returns:
    str: The name of the company if found, otherwise returns None.
    """
    # Retrieve the currently logged-in user
    user = anvil.users.get_user()

    # Proceed only if there is a logged-in user
    if user:
        # Extract the company ID from the user's record
        company_id = user.get('company_id')
        if company_id is not None:
            # Retrieve the company record using the company ID
            company = app_tables.company.get(company_id=company_id)
            if company:
                # Return the company name if the company record exists
                return company['company_name']
            else:
                # Company record does not exist for the given ID
                return None
        else:
            # The user does not have a company ID associated
            return None
    else:
        # No user is logged in
        return None








