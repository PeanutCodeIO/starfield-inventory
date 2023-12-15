from ._anvil_designer import Import_CardTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import component_cache

class Import_Card(Import_CardTemplate):
  def __init__(self, supplier_id = None,**properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id

    # Any code you write here will run before the form opens.

  def export_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.media.download(anvil.server.call('create_component_import_template', self.supplier_id))
    pass

  def file_loader_upload_template_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    file = self.file_loader_upload_template.file
    if file:
        anvil.alert(content="Allow a moment while your data is being updated", title="File Uploaded")
        
        try:
            response = anvil.server.call('upload_csv_and_create_components', file, self.supplier_id)
            anvil.alert(content="Your component list has been updated", title="Data Updated")
            
            # Refresh the supplier cache after successful upload
            component_cache.refresh_supplier_components()

        except Exception as e:
            anvil.alert(f"An error occurred: {str(e)}", title="Error")

        finally:
            self.file_loader_upload_template.clear()
          
    pass
