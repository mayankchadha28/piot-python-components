#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import os
from pathlib import Path
import logging
import ssl
import paho.mqtt.client as mqttClient

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient

class MqttClientConnector(IPubSubClient):
	"""
	MQTT Client Handler Class to handle all mqtt data.
	
	"""

	def __init__(self, clientID: str = None):
		"""
		Default constructor. This will set remote broker information and client connection
		information based on the default configuration file contents.
		
		@param clientID Defaults to None. Can be set by caller. If this is used, it's
		critically important that a unique, non-conflicting name be used so to avoid
		causing the MQTT broker to disconnect any client using the same name. With
		auto-reconnect enabled, this can cause a race condition where each client with
		the same clientID continuously attempts to re-connect, causing the broker to
		disconnect the previous instance.
		"""
		
		self.config = ConfigUtil()
		self.dataMsgListener = None

		self.host = \
			self.config.getProperty(\
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
		
		self.port = \
			self.config.getInteger(\
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_MQTT_PORT)
		
		self.keepAlive = \
			self.config.getInteger(\
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		self.defaultQos = \
			self.config.getInteger(\
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.DEFAULT_QOS_KEY, ConfigConst.DEFAULT_QOS)
		
		self.enableEncryption = \
			self.config.getBoolean(\
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.ENABLE_CRYPT_KEY)
		
		self.pemFileName = \
			self.config.getProperty(\
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.CERT_FILE_KEY)
		
		self.enableMqttClient = \
			self.config.getBoolean(\
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.ENABLE_MQTT_CLIENT_KEY)
		
		self.mqttClient = None

		if self.enableMqttClient:
			self.mqttClient = MqttClientConnector()
			self.mqttClient.setDataMessageListener(self)


		if not clientID: 
			self.clientID = \
				self.config.getProperty(\
					ConfigConst.CONSTRAINED_DEVICE, ConfigConst.DEVICE_LOCATION_ID_KEY)
		else:
			self.clientID = clientID

			
		logging.info("\tMQTT Client ID:" + self.clientID)
		logging.info("\tMQTT Broker Host:" + self.host)
		logging.info("\tMQTT Broker Port:" + str(self.port))
		logging.info("\tMQTT Keep Alive:" + str(self.keepAlive))

		__dirname = Path.cwd().parents[6] / 'cert' / 'ca.crt'
		print(__dirname)
		
#     pass


	def connectClient(self) -> bool:
		if not self.mqttClient:
			self.mqttClient = mqttClient.Client(client_id = self.clientID, clean_session = True)

			# encryption
			try:
				if self.enableEncryption:
					logging.info("Enabling TLS encryption...")

					self.port = \
						self.config.getInteger(\
							ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.SECURE_PORT_KEY, \
								  ConfigConst.DEFAULT_MQTT_SECURE_PORT)

					logging.info("..............")
					# self.mqttClient.enable_logger()
					__dirname = Path.cwd().parents[6] / 'cert' / 'ca.crt'
					self.mqttClient.tls_set(self.pemFileName, tls_version = ssl.PROTOCOL_TLS_CLIENT)
					# self.mqttClient.tls_insecure_set(True)
					
			except:
				logging.warning("Failed to enable TLS encryption. Using unencrypted connection.")

			self.mqttClient.on_connect = self.onConnect
			self.mqttClient.on_disconnect = self.onDisconnect
			self.mqttClient.on_message = self.onMessage
			self.mqttClient.on_publish = self.onPublish
			self.mqttClient.on_subscribe = self.onSubscribe

			
		if not self.mqttClient.is_connected():
			logging.info("MQTT client connecting to broker at host: "+ self.host)

			self.mqttClient.connect(self.host, self.port, self.keepAlive)
			self.mqttClient.loop_start()

			return True
		
		else:
			logging,Warning("MQTT client is already connected. Ignoring connect request.")
			return False
		
	def disconnectClient(self) -> bool:
		if self.mqttClient.is_connected():
			logging.info('Disconnecting MQTT client from broker: '+ self.host)
			self.mqttClient.loop_stop()
			self.mqttClient.disconnect()

			return True
		else:
			logging.warning('MQTT client already disconnected. Ignoring')

			return False
		
	def onConnect(self, client, userdata, flags, rc):
		logging.info("MQTT client connected to broker: "+ str(client))

		self.mqttClient.subscribe(\
			topic= ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value, qos = self.defaultQos)
		
		self.mqttClient.message_callback_add(\
			sub = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value, \
			callback = self.onActuatorCommandMessage)
		
		# self.mqttClient.
	
		
		
	def onDisconnect(self, client, userdata, rc):
		logging.info("MQTT client disconnected from broker: "+ str(client))
		
	def onMessage(self, client, userdata, msg):
		payload = msg.payload

		if payload: 
			logging.info("MQTT message received with payload: "+ str(payload.decode("utf-8")))
		else:
			logging.info("MQTT message received with no payload: "+ str(msg))
			
	def onPublish(self, client, userdata, mid):
		logging.info("MQTT message published: "+str(client))
	
	def onSubscribe(self, client, userdata, mid, granted_qos):
		logging.info("MQTT client subscribed: "+ str(client))
	
	def onActuatorCommandMessage(self, client, userdata, msg):
		"""
		This callback is defined as a convenience, but does not
		need to be used and can be ignored.
		
		It's simply an example for how you can create your own
		custom callback for incoming messages from a specific
		topic subscription (such as for actuator commands).
		
		@param client The client reference context.
		@param userdata The user reference context.
		@param msg The message context, including the embedded payload.
		"""
		logging.info('[Callback] Actuator command message received. Topic: %s.', msg.topic)

		if self.dataMsgListener:
			try:
				# all data encoded in UTF-8
				actuatorData = DataUtil().jsonToActuatorData(msg.payload.decode('utf-8'))

				logging.debug("...........ACTUATOR DATA WHEN ARRIVED........"+ str(actuatorData))

				self.dataMsgListener.handleActuatorCommandMessage(actuatorData)
			except:
				logging.exception("Failed to convert incoming actuation command payload to Actuatordata: ")
	
	def publishMessage(self, resource: ResourceNameEnum = None, msg: str = None, qos: int = ConfigConst.DEFAULT_QOS):
		# Check validity of resource (topic)
		if not resource:
			logging.warning("No topic specified. Cannot publish message.")
			return False
		
		# check validity of message
		if not msg:
			logging.warning("No message specified. Cannot publish message to topic: "+ resource.value)
			return False
		
		# check validity of QOS - set to default if necessary
		if qos < 0 or qos > 2:
			qos = ConfigConst.DEFAULT_QOS

		# publish message, and wait for publish to complete before returning
		msgInfo = self.mqttClient.publish(topic = resource.value, payload = msg, qos = qos)
		# msgInfo.wait_for_publish()
		
		return True
	
	def subscribeToTopic(self, resource: ResourceNameEnum = None, callback = None, qos: int = ConfigConst.DEFAULT_QOS):
		# check validity of resource(topic)
		if not resource:
			logging.warning("No topic specified. Cannot subscribe.")
			return False
		
		# check validity of Qos - set to default if necessary
		if qos < 0 or qos > 2:
			qos = ConfigConst.DEFAULT_QOS

		#subscribe to topic
		logging.info("Subscribing to topic %s", resource.value)
		self.mqttClient.subscribe(resource.value, qos)

		return True 
	
	def unsubscribeFromTopic(self, resource: ResourceNameEnum = None):
		# check validity of resource (topic)
		if not resource:
			logging.warning("No topic specified. Cannot unsubscribe")
			return False
		
		logging.info("Unsubscribing to topic %s", resource.value)
		self.mqttClient.unsubscribe(resource.value)

		return True

	def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
		if listener:
			self.dataMsgListener = listener

		return False
