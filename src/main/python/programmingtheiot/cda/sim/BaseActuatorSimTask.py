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

class BaseActuatorSimTask():
	"""
	Abstract class to generate common actuator data
	
	"""

	def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, simpleName: str = "Actuator"):
		
		self.latestActuatorResponse = ActuatorData(typeID= typeID, name= name)
		self.latestActuatorResponse.setAsResponse()

		self.name = name
		self.typeID = typeID
		self.simpleName = simpleName
		self.lastKnownCommand = ConfigConst.DEFAULT_COMMAND
		self.lastKnownValue = ConfigConst.DEFAULT_VAL
		
	def getLatestActuatorResponse(self) -> ActuatorData:
		"""
		This can return the current ActuatorData response instance or a copy.
		"""
		return self.latestActuatorResponse
	
	def getSimpleName(self) -> str:
		return self.simpleName
	
	def updateActuator(self, data: ActuatorData) -> ActuatorData:
		"""
		NOTE: If 'data' is valid, the actuator-specific work can be delegated
		as follows:
		 - if command is ON: call self._activateActuator()
		 - if command is OFF: call self._deactivateActuator()
		
		Both of these methods will have a generic implementation (logging only) within
		this base class, although the sub-class may override if preferable.
		"""

		if data and self.typeID == data.getTypeID():
			statusCode = ConfigConst.DEFAULT_STATUS

			curCommand = data.getCommand()
			curVal = data.getValue()

			logging.info(".........."+ str(curCommand)+" "+ str(curVal)+ "...........")

			#check if command is repeat. if yes then skip
			if curCommand == self.lastKnownCommand and curVal == self.lastKnownValue:
				logging.debug(\
					"New actuator command and value is repeated. Ignoring: %s %s", \
					str(curCommand), str(curVal)
				)
			else:
				logging.debug(\
					"New actuator command and value to be applied: %s %s", \
					str(curCommand), str(curVal)
				)

				logging.info(".......Current COMMAND: "+ str(curCommand)+"....")
				if curCommand == ConfigConst.COMMAND_ON:
					#ON state
					logging.info(".......Activating Actuator...............")
					statusCode = self._activateActuator(val= data.getValue(), stateData= data.getStateData)
					
					
				elif curCommand == ConfigConst.COMMAND_OFF:
					#OFF state
					logging.info("......Deactivating actuator...")
					statusCode = self._deactivateActuator(val= data.getValue(),\
										    stateData=data.getStateData())
				
				else:
					#Error State
					logging.warning("ActuatorData command is unknnown, Ignoring: %s", str(curCommand))
					statusCode = -1

				#updating last known actuator command and value
				self.lastKnownCommand = curCommand
				self.lastKnownValue = curVal

				#creating the ActuatorData response from the command
				actuatorResponse = ActuatorData()
				actuatorResponse.updateData(data)
				actuatorResponse.setStatusCode(statusCode)
				actuatorResponse.setAsResponse()

				self.latestActuatorResponse.updateData(actuatorResponse)

				return actuatorResponse
			
		return None

	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Private method for actuator ON functionality & log messages
		
		@param val The actuation activation value to process.
		@param stateData The string state data to use in processing the command.
		"""
		logging.debug("..............Entered Activate Actuator.........................")
		msg = "\n*****"
		msg = msg + "\n* 0 N *"
		msg = msg + "\n*****"
		msg = msg + "\n" + self.name + "VALUE -> " + str(val) + "\n====="

		logging.info("Simulating %s actuator ON: %s", self.name, msg)

		return 0

		
	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Actuator OFF functionality & logging messages 
		
		@param val The actuation activation value to process.
		@param stateData The string state data to use in processing the command.
		"""
		msg = "\n*****"
		msg = msg + "\n* OFF *"
		msg = msg + "\n*****"

		logging.info("Simulating %s actuator OFF: %s", self.name, msg)

		return 0
		