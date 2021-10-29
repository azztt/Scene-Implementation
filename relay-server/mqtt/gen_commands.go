package mqtt

import (
	"encoding/json"
	"fmt"

	CONFIG "github.com/azztt/Scene-Implementation/config"
	DB "github.com/azztt/Scene-Implementation/database"
	MODELS "github.com/azztt/Scene-Implementation/models"
	MQTT "github.com/eclipse/paho.mqtt.golang"
)

type room struct {
	ID   string
	Name string
}

// callback for new room creation acknowledgement
func OnNewRoomAck(client MQTT.Client, message MQTT.Message) {
	// first unsubscribe from the topic
	client.Unsubscribe(CONFIG.NEW_ROOM_ACK)

	var room room
	var done bool = true
	err := json.Unmarshal(message.Payload(), &room)
	if err != nil {
		fmt.Println("Could not verify new room creation")
		done = false
	}

	if done {
		var newRoom MODELS.Room = MODELS.Room{
			ID:        room.ID,
			Name:      room.Name,
			DeviceIds: make([]string, 0),
		}
		// writing to database
		err := DB.InsertNewRoom(newRoom)
		if err != nil {
			fmt.Println("Could not write room to database")
			return
		}
		/*
			TODO:
				broadcast acknowledgement to frontend
		*/
	}
}

// sends command for new room creation
func NewRoom(roomName string) {
	// subscribe to acknowledge topic
	client.Subscribe(
		CONFIG.NEW_ROOM_ACK,
		byte(CONFIG.MQTT_QOS),
		OnNewRoomAck,
	)

	client.Publish(
		CONFIG.NEW_ROOM,
		byte(CONFIG.MQTT_QOS),
		false,
		roomName,
	)
}

// callback for room deletion acknowledgement
func OnRemRoomAck(client MQTT.Client, message MQTT.Message) {
	// first unsubscribe from the topic
	client.Unsubscribe(CONFIG.REM_ROOM_ACK)

	var done bool = true
	var roomId string = string(message.Payload())

	if roomId == "failed" {
		done = false
	}

	if done {
		// deleting from database
		err := DB.DeleteRoomById(roomId)
		if err != nil {
			fmt.Println("Could not delete room from database")
			return
		}
		/*
			TODO:
				broadcast acknowledgement to frontend
		*/
	}
}

// sends command for new room creation
func RemoveRoom(roomId string) {
	// subscribe to acknowledge topic
	client.Subscribe(
		CONFIG.REM_ROOM_ACK,
		byte(CONFIG.MQTT_QOS),
		OnRemRoomAck,
	)

	client.Publish(
		CONFIG.REM_ROOM,
		byte(CONFIG.MQTT_QOS),
		false,
		roomId,
	)
}

// callback for new device acknowledgement
func OnNewDeviceAck(client MQTT.Client, message MQTT.Message) {
	// first unsubscribe from the topic
	client.Unsubscribe(CONFIG.NEW_DEVICE_ACK)

	var done bool = true
	var msg map[string]interface{}
	err := json.Unmarshal(message.Payload(), &msg)

	if err != nil {
		done = false
	}

	if done {
		// insert device in the database
		var device MODELS.Device = MODELS.Device{
			ID:         msg["id"].(string),
			Name:       msg["name"].(string),
			Type:       msg["type"].(string),
			Parameters: msg["parameters"].(string),
			Status:     msg["status"].(string),
		}
		err := DB.InsertNewDevice(device)
		if err != nil {
			fmt.Println("Could not add device to database")
			return
		}

		// added to list of online devices
		onlineDevices[device.ID] = mem

		/*
			TODO:
				broadcast acknowledgement to frontend
		*/
	}
}

// sends command for new device creation
func NewDevice(params map[string]interface{}) {
	var dType string = params["type"].(string)

	jsonData, _ := json.Marshal(params)
	// subscribe to acknowledgement topic

	client.Publish(
		CONFIG.NEW_DEVICE,
		byte(CONFIG.MQTT_QOS),
		false,
		jsonData,
	)
	if dType == MODELS.AC_TYPE {
		var ac MODELS.AC
		ac.CreateDevice(params)
	} else if dType == MODELS.CLIGHT_TYPE {
		var clight MODELS.ColorLight
		clight.CreateDevice(params)
	} else if dType == MODELS.FAN_TYPE {
		var fan MODELS.Fan
		fan.CreateDevice(params)
	} else if dType == MODELS.LIGHT_TYPE {
		var light MODELS.Light
		light.CreateDevice(params)
	} else if dType == MODELS.DLOCK_TYPE {
		// var dlock MODELS.ColorLight
	}
}

// callback for room deletion acknowledgement
func OnRemDeviceAck(client MQTT.Client, message MQTT.Message) {
	// first unsubscribe from the topic
	client.Unsubscribe(CONFIG.REM_DEVICE_ACK)

	var done bool = true
	var deviceId string = string(message.Payload())

	if deviceId == "failed" {
		done = false
	}

	if done {
		// deleting from database
		err := DB.DeleteDeviceById(deviceId)
		if err != nil {
			fmt.Println("Could not delete device from database")
			return
		}
		// removing from server lists
		delete(onlineDevices, deviceId)
		delete(acs, deviceId)
		delete(colorLights, deviceId)
		delete(doorLocks, deviceId)
		delete(fans, deviceId)
		delete(lights, deviceId)
		/*
			TODO:
				broadcast acknowledgement to frontend
		*/
	}
}

// sends command for new room creation
func RemoveDevice(deviceId string) {
	// subscribe to acknowledge topic
	client.Subscribe(
		CONFIG.REM_DEVICE_ACK,
		byte(CONFIG.MQTT_QOS),
		OnRemDeviceAck,
	)

	client.Publish(
		CONFIG.REM_DEVICE,
		byte(CONFIG.MQTT_QOS),
		false,
		deviceId,
	)
}
