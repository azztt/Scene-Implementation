package mqtt

import (
	"encoding/json"
	"fmt"

	CONFIG "github.com/azztt/Scene-Implementation/config"
	DB "github.com/azztt/Scene-Implementation/database"
	MODELS "github.com/azztt/Scene-Implementation/models"
	MQTT "github.com/eclipse/paho.mqtt.golang"
)

// callback for new room creation acknowledgement
func OnNewRoomAck(client MQTT.Client, message MQTT.Message) (MODELS.Room, error) {
	// first unsubscribe from the topic
	client.Unsubscribe(CONFIG.NEW_ROOM_ACK)

	var room MODELS.Room
	// var done bool = true
	err := json.Unmarshal(message.Payload(), &room)
	if err != nil {
		fmt.Println("Could not verify new room creation")
		// done = false
		return room, err
	}

	// writing to database
	err = DB.InsertNewRoom(room)
	if err != nil {
		fmt.Println("Could not write room to database")
		return room, err
	}
	return room, nil
}

// sends command for new room creation
func NewRoom(roomName string) (MODELS.Room, error) {
	var room MODELS.Room
	var err error
	done := false
	// subscribe to acknowledge topic
	client.Subscribe(
		CONFIG.NEW_ROOM_ACK,
		byte(CONFIG.MQTT_QOS),
		func(c MQTT.Client, m MQTT.Message) {
			room, err = OnNewRoomAck(c, m)
			done = true
		},
	)

	client.Publish(
		CONFIG.NEW_ROOM,
		byte(CONFIG.MQTT_QOS),
		false,
		roomName,
	)

	for {
		if done {
			break
		}
	}

	if err != nil {
		return room, err
	} else {
		return room, nil
	}
}

// callback for room deletion acknowledgement
func OnRemRoomAck(client MQTT.Client, message MQTT.Message) error {
	// first unsubscribe from the topic
	client.Unsubscribe(CONFIG.REM_ROOM_ACK)

	var done bool = true
	var roomId string = string(message.Payload())

	if roomId == "failed" {
		done = false
	}

	if done {
		// deleting room from database, cascade delete enabled
		err := DB.DeleteRoomById(roomId)
		if err != nil {
			fmt.Println("Could not delete room from database")
			return err
		}
		return nil
	}
	return fmt.Errorf("removing room failed")
}

// sends command for removing room
func RemoveRoom(roomId string) error {
	var err error
	done := false
	// subscribe to acknowledge topic
	client.Subscribe(
		CONFIG.REM_ROOM_ACK,
		byte(CONFIG.MQTT_QOS),
		func(c MQTT.Client, m MQTT.Message) {
			err = OnRemRoomAck(c, m)
			done = true
		},
	)

	client.Publish(
		CONFIG.REM_ROOM,
		byte(CONFIG.MQTT_QOS),
		false,
		roomId,
	)

	for {
		if done {
			break
		}
	}

	if err != nil {
		return err
	} else {
		return nil
	}
}

// creating new scene information
func NewScene(sceneInfo map[string]interface{}) {
	/*
		sceneInfo {
			"name": string,
			"deviceConfigs": [
				{
					"deviceId": string,
					"config": string
				},...
			]
		}
	*/
	var deviceConfigs []interface{} = sceneInfo["deviceConfigs"].([]interface{})
	// adding a new scene first in db
	newSceneId, err := DB.InsertNewScene(MODELS.Scene{
		Name: sceneInfo["name"].(string),
	})

	if err != nil {
		fmt.Println("Could not create scene in database")
		return
	}

	// add configs to db
	err = DB.InsertNewConfigs(newSceneId, deviceConfigs)
	if err != nil {
		fmt.Println("Could not add configs to database")
		return
	}
}

// callback for new device acknowledgement
func OnNewDeviceAck(client MQTT.Client, message MQTT.Message) (MODELS.Device, error) {
	// first unsubscribe from the topic
	client.Unsubscribe(CONFIG.NEW_DEVICE_ACK)

	// var done bool = true
	var msg map[string]interface{}
	var err error
	if string(message.Payload()) == "FAILED" {
		err = fmt.Errorf("could not create device in simulation")
		return MODELS.Device{}, err
	}
	err = json.Unmarshal(message.Payload(), &msg)

	if err != nil {
		// done = false
		fmt.Printf("error in unmarhsalling: %v\n", err)
		return MODELS.Device{}, err
	}

	fmt.Printf("new device ack msg:\n%v\n", msg)

	// if done {
	// insert device in the database
	var device MODELS.Device = MODELS.Device{
		ID:         msg["id"].(string),
		Name:       msg["name"].(string),
		RoomId:     msg["roomId"].(string),
		Type:       msg["type"].(string),
		Parameters: msg["parameters"].(string),
		Status:     structToStatusString(msg["status"].(map[string]interface{})),
	}
	err = DB.InsertNewDevice(device)
	if err != nil {
		fmt.Println("Could not add device to database")
		return MODELS.Device{}, err
	}

	// added to list of online devices
	// onlineDevices[device.ID] = mem
	fmt.Printf("device added to database:\n%v\n", device)
	return device, nil
	// }
}

// sends command for new device creation
func NewDevice(params map[string]interface{}) (MODELS.Device, error) {
	// var dType string = params["type"].(string)
	done := false
	var device MODELS.Device
	var err error

	jsonData, _ := json.Marshal(params)
	// subscribe to acknowledgement topic
	client.Subscribe(
		CONFIG.NEW_DEVICE_ACK,
		byte(CONFIG.MQTT_QOS),
		func(c MQTT.Client, m MQTT.Message) {
			device, err = OnNewDeviceAck(c, m)
			done = true
		},
	)

	client.Publish(
		CONFIG.NEW_DEVICE,
		byte(CONFIG.MQTT_QOS),
		false,
		jsonData,
	)

	for {
		if done {
			break
		}
	}
	if err != nil {
		return device, err
	}
	return device, nil
	// if dType == MODELS.AC_TYPE {
	// 	var ac MODELS.AC
	// 	ac.CreateDevice(params)
	// } else if dType == MODELS.CLIGHT_TYPE {
	// 	var clight MODELS.ColorLight
	// 	clight.CreateDevice(params)
	// } else if dType == MODELS.FAN_TYPE {
	// 	var fan MODELS.Fan
	// 	fan.CreateDevice(params)
	// } else if dType == MODELS.LIGHT_TYPE {
	// 	var light MODELS.Light
	// 	light.CreateDevice(params)
	// }
	// else if dType == MODELS.DLOCK_TYPE {
	// var dlock MODELS.ColorLight
	// }
}

// callback for deletion deletion acknowledgement
func OnRemDeviceAck(client MQTT.Client, message MQTT.Message) error {
	// first unsubscribe from the topic
	client.Unsubscribe(CONFIG.REM_DEVICE_ACK)

	var done bool = true
	var deviceId string = string(message.Payload())

	if deviceId == "failed" {
		done = false
	}

	if done {
		// deleting from database, cascade delete enabled
		err := DB.DeleteDeviceById(deviceId)
		if err != nil {
			fmt.Println("Could not delete device from database")
			return err
		}
		// removing from server lists
		delete(onlineDevices, deviceId)
		delete(acs, deviceId)
		delete(colorLights, deviceId)
		delete(doorLocks, deviceId)
		delete(fans, deviceId)
		delete(lights, deviceId)
		return nil
	}
	return fmt.Errorf("removing device failed")
}

// sends command for device deletion
func RemoveDevice(deviceId string) error {
	done := false
	var err error
	// subscribe to acknowledge topic
	client.Subscribe(
		CONFIG.REM_DEVICE_ACK,
		byte(CONFIG.MQTT_QOS),
		func(c MQTT.Client, m MQTT.Message) {
			err = OnRemDeviceAck(c, m)
			done = true
		},
	)

	client.Publish(
		CONFIG.REM_DEVICE,
		byte(CONFIG.MQTT_QOS),
		false,
		deviceId,
	)

	for {
		if done {
			break
		}
	}

	if err != nil {
		return err
	} else {
		return nil
	}
}
