from ._anvil_designer import Import_CardTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .... import supplier_cache

class Import_Card(Import_CardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def export_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.media.download(anvil.server.call('create_suppliers_import_template'))
    pass

  def file_loader_upload_template_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    file = self.file_loader_upload_template.file
    if file:
        response = anvil.server.call('upload_csv_and_create_suppliers', file)

        self.file_loader_upload_template.clear()
        anvil.alert(content="Allow some time while the data is updated", title="File Uploaded")

    supplier_cache.refresh_all_suppliers()

    pass
