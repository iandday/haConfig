import appdaemon.plugins.hass.hassapi as hass

#
# App to dynamically show or hide a group based on an entity value
#
# Created to only show a group of media player controls only when the player is in use
#
# Args:
#   entity: entity to monitor
#   hidden_value: value of the entity to monitor which will triger hiding of the specified group
#   group: group to be shown or hidden
#
# Release Notes
#   Version 1.0: Initial Version

class HideGroup(hass.Hass):
  '''Hide/Show a group based on an entity value'''

  def initialize(self):
    self._entity = self.args['entity']
    self._hidden_value = self.args['hidden_value']
    self._group = self.args['group']
  
    self.listen_state(self.receive_current_state, self._entity)
    self.log('Initialization complete, monitoring ' + self._entity + ' for group ' + self._group, level = 'INFO')

  
  def receive_current_state(self, entity, attribute, old, new,*args):
    self.value = self.get_state(self._entity)
    if self.value == self._hidden_value:
        self.call_service("group/set_visibility", entity_id = self._group, visible = 'false')
        self.log('Hiding group ' + self._group, level='DEBUG')   
    else: 
        self.call_service("group/set_visibility", entity_id = self._group, visible = 'true')
        self.log('Showing group ' + self._group, level='DEBUG')
        
        
      