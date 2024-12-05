#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.BaseIotData import BaseIotData

class ActuatorData(BaseIotData):
	"""
	Class implementation for setting the data containers for simulating actuator data
	
	"""


	def __init__(self, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, name = ConfigConst.NOT_SET, d = None):
		super(ActuatorData, self).__init__(name = name, typeID = typeID, d = d)
		
		#Defining class variables
		self.value = ConfigConst.DEFAULT_VAL
		self.command = ConfigConst.DEFAULT_COMMAND
		self.stateData = ""


		pass
	
	def getCommand(self) -> int:
		return self.command
	
	def getStateData(self) -> str:
		return self.stateData
	
	def getValue(self) -> float:
		return self.value
	
	def isResponseFlagEnabled(self) -> bool:
		return False
	
	def setCommand(self, command: int):
		#Set command values & Timestamp
		self.command = command
		self.updateTimeStamp()

	
	def setAsResponse(self):
		"""
		set response flat True
		"""
		self.isResponse = True
		self.updateTimeStamp()
		
	def setStateData(self, stateData: str):
		if stateData:
			self.stateData = stateData
			self.updateTimeStamp()

	
	def setValue(self, val: float):
		self.value = val
		self.updateTimeStamp()
		
	# Private method to update variables
	def _handleUpdateData(self, data):
		#verifying instances and updating variables if not then its invoked by base class
		if data and isinstance(data, ActuatorData):
			self.command = data.getCommand()
			self.stateData = data.getStateData()
			self.value = data.getValue()
			self.isResponse = data.isResponseFlagEnabled()
		