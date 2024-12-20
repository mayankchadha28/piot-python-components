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

class SystemPerformanceData(BaseIotData):
	"""
	Class implementation for storing system performance data
	
	"""
	DEFAULT_VAL = 0.0
	
	def __init__(self, d = None):
		super(SystemPerformanceData, self).__init__(name = ConfigConst.SYSTEM_PERF_MSG, typeID = ConfigConst.SYSTEM_PERF_TYPE, d = d)
		
		self.cpuUtil = ConfigConst.DEFAULT_VAL
		self.memUtil = ConfigConst.DEFAULT_VAL
		self.diskUtil = ConfigConst.DEFAULT_VAL
	
	def getCpuUtilization(self):
		return self.cpuUtil
	
	def getDiskUtilization(self):
		return self.diskUtil
	
	def getMemoryUtilization(self):
		return self.memUtil
	
	def setCpuUtilization(self, cpuUtil):
		self.cpuUtil = cpuUtil
		self.updateTimeStamp()
	
	def setDiskUtilization(self, diskUtil):
		self.diskUtil = diskUtil
		self.updateTimeStamp()
	
	def setMemoryUtilization(self, memUtil):
		self.memUtil = memUtil
		self.updateTimeStamp()
	
	def _handleUpdateData(self, data):
		# Setting the values like cpu, memory and disk utilization
		if data and isinstance(data, SystemPerformanceData):
			self.cpuUtil = data.getCpuUtilization()
			self.memUtil = data.getMemoryUtilization()
			self.diskUtil = data.getDiskUtilization()
