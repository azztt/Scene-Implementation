package config

// client config
const MQTT_SERVER string = "localhost"
const MQTT_PORT int = 1883
const MQTT_QOS int = 1
const MQTT_CLIENT_ID string = "RELAY_SERVER"

// topics for simulation
const PRES_SIM string = "simulation/connected"
const CONT_CON string = "simulation/sub"
const CONT_DISCON string = "simulation/unsub"
const NEW_ROOM string = "simulation/new_room"
const NEW_ROOM_ACK string = "simulation/new_room/ack"
const REM_ROOM string = "simulation/rem_room"
const REM_ROOM_ACK string = "simulation/rem_room/ack"
const NEW_DEVICE string = "simulation/new_device"
const NEW_DEVICE_ACK string = "simulation/new_device/ack"
const REM_DEVICE string = "simulation/rem_device"
const REM_DEVICE_ACK string = "simulation/rem_device/ack"
const DEVICE_STATUS string = "simulation/device_status/+"
const START_SIM string = "simulation/start"
const STOP_SIM string = "simulation/stop"

// topics for device controllers
const DEVICE_COMMAND string = "simulation/device_command"

const MQTT_WILL_TOPIC string = "simulation/will"

// topic utility methods

func GetDeviceComTopic(deviceID string) string {
	return DEVICE_COMMAND
}

func GetDeviceAckTopic(deviceID string) string {
	return DEVICE_COMMAND + "/" + deviceID + "/ack"
}
