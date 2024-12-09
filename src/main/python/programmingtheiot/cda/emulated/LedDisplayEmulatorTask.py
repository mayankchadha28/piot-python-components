#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from pisense import SenseHAT

class LedDisplayEmulatorTask(BaseActuatorSimTask):
	"""
	This class emulates the LED Actuator using the SenseHat
	
	"""

	def __init__(self):
		super(\
			LedDisplayEmulatorTask, self).__init__(
				name= ConfigConst.LED_ACTUATOR_NAME,
				typeID = ConfigConst.LED_DISPLAY_ACTUATOR_TYPE, \
				simpleName= "LED_Display"
			)
		
		enableEmulation = \
			ConfigUtil().getBoolean(\
				ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.sh = SenseHAT(emulate = enableEmulation)

	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		#logging.debug("...........I am at LED. ..................")
		
		BaseActuatorSimTask._activateActuator(self, val = val, stateData= stateData)
		
		# logging.debug(stateData)
		if self.sh.screen:
			self.sh.screen.scroll_text("LED Switching ON", size = 8)
			return 0
		else:
			logging.warning("No SenseHat LED screen instance to write.")
			return -1

	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		
		BaseActuatorSimTask._activateActuator(self, val = val, stateData= stateData)

		if self.sh.screen:
			self.sh.screen.clear()
			return 0
		else: 
			logging.warning("No SenseHat LED screen instance to clear.")
			return -1
	