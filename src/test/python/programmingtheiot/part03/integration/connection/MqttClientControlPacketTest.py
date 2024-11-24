import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData 
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData 
from programmingtheiot.data.DataUtil import DataUtil

class MqttClientControlPacketTest(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Executing the MqttClientControlPacketTest class...")
		
		self.cfg = ConfigUtil()
		
		# NOTE: Be sure to use a DIFFERENT clientID than that which is used
		# for your CDA when running separately from this test
		# 
		# The clientID shown below is an example only - please use your own
		# unique value for this test
	
		self.mcc = MqttClientConnector(clientID="TestClient")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testConnectAndDisconnect(self):
	    # TODO: implement this test
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		self.mcc.connectClient()
		sleep(delay +5)
		self.mcc.disconnectClient()
	
	
	def testServerPing(self):
		# TODO: implement this test
		pass
	
	def testPubSub(self):
		# TODO: implement this test
		# 
		# IMPORTANT: be sure to use QoS 1 and 2 to see ALL control packets
		pass	
	
if __name__ == "__main__":
	unittest.main()