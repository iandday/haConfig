import appdaemon.plugins.hass.hassapi as hass

#
# App to turn lights on when motion detected then off again after a delay
#
# Use with constrints to activate only for the hours of darkness
#
# Args:
#   sensor: binary sensor to use as trigger
#   entity_on : entity to turn on when detecting motion, can be a light, script, scene or anything else that can be turned on
#   entity_off : entity to turn off when detecting motion, can be a light, script or anything else that can be turned off. Can also be a scene which will be turned on
#   delay: amount of time after turning on to turn off again. If not specified defaults to 60 seconds.
#   constraint_sensor: 
#   constraint_value:
# 
# Release Notes
#   Version 1.1:  Add ability for other apps to cancel the timer
#   Version 1.0: Initial Version

class MotionLights(hass.Hass):

  def initialize(self):
    
    self.handle = None

    if 'delay' in self.args:
        self._delay = self.args['delay']
    else:
        self._delay = 60

    if 'constraint_sensor' in self.args:
        self._csensor = self.args['constraint_sensor']
    else:
        self._csensor = None
    if 'constraint_value' in self.args:
        self._cvalue = self.args['constraint_value']
    else:
        self._cvalue = None
    if 'sensor' in self.args:
      self.listen_state(self.motion, self.args['sensor'])
      self.log('Monitoring sensor {}'.format(self.args['sensor']))
    else:
      self.log('No sensor specified')
    

  def motion(self, entity, attribute, old, new, kwargs):
    if new == 'on':
      if 'entity_on' in self.args:
        if self._csensor:
            if self.get_state(self.args['constraint_sensor']) == self.args['constraint_value']:
                self.log('Motion detected: turning {} on'.format(self.args['entity_on']))
                self.turn_on(self.args['entity_on'])
                self.cancel_timer(self.handle)
                self.handle = self.run_in(self.light_off, self._delay)
            else: 
                self.log('Motion detected but constraint sensor prevented activation')

        else:     
                self.log('Motion detected: turning {} on'.format(self.args['entity_on']))
                self.turn_on(self.args['entity_on'])
                self.cancel_timer(self.handle)
                self.handle = self.run_in(self.light_off, self._delay) 

  def light_off(self, kwargs):
    #if 'entity_off' in self.args:
    self.log('Turning {} off'.format(self.args['entity_on']))
    self.turn_off(self.args['entity_on'])
        

  def cancel(self):
    self.cancel_timer(self.handle)
      
