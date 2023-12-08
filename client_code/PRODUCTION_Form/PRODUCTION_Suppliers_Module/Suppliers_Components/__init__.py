from ._anvil_designer import Suppliers_ComponentsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Import_Card import Import_Card
from .Component_List import Component_List
from .New_Component import New_Component

class Suppliers_Components(Suppliers_ComponentsTemplate):
  def __init__(self, supplier_id = None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.supplier_id = supplier_id

    # Any code you write here will run before the form opens.
    cmpt = Component_List()
    self.content_panel.clear()
    self.content_panel.add_component(cmpt)

  def add_cmpt_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module.Suppliers_Components.New_Component', self.supplier_id)
    pass

  def import_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    cmpt = Import_Card()
    self.content_panel.clear()
    self.content_panel.add_component(cmpt)
    pass

  def exit_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('PRODUCTION_Form.PRODUCTION_Suppliers_Module', self.supplier_id)
    pass

  def cmpt_list_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    cmpt = Component_List()
    self.content_panel.clear()
    self.content_panel.add_component(cmpt)
    pass
