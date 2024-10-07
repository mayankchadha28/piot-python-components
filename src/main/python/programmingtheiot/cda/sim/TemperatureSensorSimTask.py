#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

import programmingtheiot.common.ConfigConst as COnfigConst

from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

from programmingtheiot.data.SensorData import SensorData

class TemperatureSensorSimTask(BaseSensorSimTask):
	"""
	initializing the constructor for the base class along with all the parameters
	
	"""

	def __init__(self, dataSet=None):
		super(TemperatureSensorSimTask, self).__init__(\
			name= COnfigConst.TEMP_SENSOR_NAME, \
			typeID= COnfigConst.TEMP_SENSOR_TYPE, \
			dataSet= dataSet, \
			minVal= SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP, \
			maxVal= SensorDataGenerator.HI_NORMAL_INDOOR_TEMP \
		)
	