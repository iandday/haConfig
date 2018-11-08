import appdaemon.plugins.hass.hassapi as hass
from homeassistant.components.media_player.kodi import (
    EVENT_KODI_CALL_METHOD_RESULT)


#
# App to populate list of PVR channels for a Kodi player and launch channel once selected
#
# Adopted from https://www.home-assistant.io/cookbook/automation_kodi_dynamic_input_select/
#
# Args:
#   source: input select object to populate and monitor for selection
#   target: kodi media player
#
# Release Notes
#   Version 1.0: Initial Version


DEFAULT_ACTION = '-'
MAX_RESULTS = 80

class DynamicKodiInputSelect(hass.Hass):

    def initialize(self):
        """Set up appdaemon app."""
        self._source = self.args['source']
        self._target = self.args['target']
        self.listen_event(self._receive_kodi_result,
                          EVENT_KODI_CALL_METHOD_RESULT)
        self.listen_state(self._change_selected_option, self._source)
        self._ids_options = {DEFAULT_ACTION: None}
        self.log('Initialization complete, monitoring: ' + self._source, level = 'DEBUG')


    def _receive_kodi_result(self, event_id, payload_event, *args):
        result = payload_event['result']
        method = payload_event['input']['method']
        entity = payload_event['entity_id']

        assert event_id == EVENT_KODI_CALL_METHOD_RESULT
        if method == 'PVR.GetChannels' and entity == self._target:
            self.log(payload_event, level = 'DEBUG')
            values = result['channels']
            data = [(r['label'], ('CHANNEL', r['channelid']))
                    for r in values]
            self._ids_options.update(dict(zip(*zip(*data))))
            labels = list(list(zip(*data))[0])
            self.call_service('input_select/set_options',
                              entity_id = self._source,
                              options = [DEFAULT_ACTION] + labels)
            self.set_state(self._source,
                           attributes={"friendly_name": 'TV channels',
                                       "icon": 'mdi:play-box-outline'})


    def _change_selected_option(self, entity, attribute, old, new, kwargs):
        self.log('New Channel Label' + str(self._ids_options), level = 'DEBUG')
        self.log('New Channel Number' + str(new), level = 'DEBUG')
        
        selected = self._ids_options[new]
        if selected:
            mediatype, file = selected
            self.call_service('media_player/play_media',
                              entity_id = self._target,
                              media_content_type = mediatype,
                              media_content_id = file)

