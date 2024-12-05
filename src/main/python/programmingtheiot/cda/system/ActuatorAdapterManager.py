#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

from programmingtheiot.cda.emulated.HvacEmulatorTask import HvacEmulatorTask


class ActuatorAdapterManager(object):
	"""
		Main class that instantiates all actuators - 
		Hvac, Humidifier etc and is responsible for sending actuator commands
	
	"""
	
	def __init__(self, dataMsgListener: IDataMessageListener= None):
		self.dataMsgListener = dataMsgListener

		self.configUtil = ConfigUtil()

		self.useSimulator = \
			self.configUtil.getBoolean(\
				section= ConfigConst.CONSTRAINED_DEVICE, key= ConfigConst.ENABLE_SIMULATOR_KEY)
		
		self.useEmulator = \
			self.configUtil.getBoolean(\
				section= ConfigConst.CONSTRAINED_DEVICE, key= ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.deviceID = \
			self.configUtil.getProperty(\
				section= ConfigConst.CONSTRAINED_DEVICE, key= ConfigConst.DEVICE_LOCATION_ID_KEY, \
					defaultVal=ConfigConst.NOT_SET)
		
		self.locationID = \
			self.configUtil.getProperty(\
				section= ConfigConst.CONSTRAINED_DEVICE, key= ConfigConst.DEVICE_LOCATION_ID_KEY, \
					defaultVal=ConfigConst.NOT_SET)
		
		self.humidifierActuator = None
		self.hvacActuator = None
		self.ledDisplayActuator = None

		self._initEnvironmentalActuationTasks()

		

	def sendActuatorCommand(self, data: ActuatorData) -> ActuatorData:
		if data and not data.isResponseFlagEnabled():
			
			if data.getLocationID() == self.locationID:
				logging.info("Actuator command received for location ID %s. Processing...", \
				 str(data.getLocationID()))
				
				aType  = data.getTypeID()
				responseData = None
			
				if aType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and self.humidifierActuator:
					responseData = self.humidifierActuator.updateActuator(data)
				elif aType == ConfigConst.HVAC_ACTUATOR_TYPE and self.hvacActuator:
					responseData = self.hvacActuator.updateActuator(data)
				elif aType == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and self.ledDisplayActuator:
					#TODO: Implement led actuator
					responseData = self.ledDisplayActuator.updateActuator(data)
					pass
				else:
					logging.warning("No valid actuator type. Ignoring actuation for type: %s", data.getTypeID())
				
				return responseData
			
			else: 
				logging.warning("Location ID does'nt match. Ignoring actuation: %s != %s", str(self.locationID), str(data.getLocationID))

		else:
			logging.warning("Actuator request received. Message is empty or response. Ignoring.")

		return None
	
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if listener:
			self.dataMsgListener = listener

	def _initEnvironmentalActuationTasks(self):
		if not self.useEmulator:
			self.humidifierActuator = HumidifierActuatorSimTask()

			self.hvacActuator = HvacActuatorSimTask()
		else:
			# Emulator Functionality
			
			# Humidifier
			hueModule = import_module('programmingtheiot.cda.emulated.HumidifierEmulatorTask', \
							 'HumidifierEmulatedTask')
			hueClass = getattr(hueModule, 'HumidifierEmulatorTask')
			self.humidifierActuator = hueClass()

			# HVAC
			self.hvacActuator = HvacEmulatorTask()
			# hveModule = import_module('programmingtheiot.cda.emulated.HvacEmulatorTask', \
			# 				 'HvacEmulatorTask')
			# hveClass = getattr(hveModule, 'HvacEmulatorTask')
			# self.hvacActuator = hveClass()

			# LED
			leDisplayModule = import_module('programmingtheiot.cda.emulated.LedDisplayEmulatorTask', \
								   'LedDisplayEmulatorTask')
			leClass = getattr(leDisplayModule, 'LedDisplayEmulatorTask')
			self.ledDisplayActuator = leClass()


