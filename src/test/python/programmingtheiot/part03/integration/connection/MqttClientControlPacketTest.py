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

		
	def setUp(self):
		self.mcc = MqttClientConnector(clientID="MqttClientControlPacketTest")

	def tearDown(self):
		pass

	def testConnectAndDisconnect(self):

		self.assertTrue(self.mcc.connectClient())
		sleep(5)
		self.assertTrue(self.mcc.disconnectClient())

		logging.info("Mqtt Connect and Disconnect")

	
	def testServerPing(self):
		delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		self.assertTrue(self.mcc.connectClient())
		logging.info("Connected to MQTT Broker")
		sleep(delay +5)
		self.assertTrue(self.mcc.disconnectClient())
		logging.info("Server ping triggered")
		
	
	def testPubSub(self):
		self.assertTrue(self.mcc.connectClient())
		qos_0 = 0
		qos_1 = 1
		qos_2 = 2

		sensorData = SensorData()
		payload = DataUtil().sensorDataToJson(sensorData)

		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, \
								  msg = payload, qos = qos_0)
		logging.info("Mqtt Message published with QOS 0")
		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, \
								  msg = payload, qos = qos_1)
		logging.info("Mqtt Message published with QOS 1")
		self.mcc.publishMessage(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, \
								  msg = payload, qos = qos_2)
		logging.info("Mqtt Message published with QOS 2")

		logging.info("MQTT Message Subscribed with QOS 0")
		self.mcc.subscribeToTopic(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, \
								qos = qos_0)
		
		logging.info("MQTT Message Subscribed with QOS 0")
		self.mcc.subscribeToTopic(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, \
								qos = qos_1)
		
		logging.info("MQTT Message Subscribed with QOS 0")
		self.mcc.subscribeToTopic(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, \
								qos = qos_2)
		
		self.mcc.unsubscribeFromTopic(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE)

		sleep(5)
		
		self.assertTrue(self.mcc.disconnectClient())


		
	
if __name__ == "__main__":
	unittest.main()