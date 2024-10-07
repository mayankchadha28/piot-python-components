#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import random

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

class HvacActuatorSimTask(BaseActuatorSimTask):
	"""
		The class simulates the actuator for the HVAC 
	
	"""

	def __init__(self):
		super().__init__(\
			name= ConfigConst.HVAC_ACTUATOR_NAME,
			typeID= ConfigConst.HVAC_ACTUATOR_TYPE, \
			simpleName= "HVAC"
		)
		