package mqtt

import (
	"encoding/json"
	"fmt"
	"strings"

	DB "github.com/azztt/Scene-Implementation/database"
	MODELS "github.com/azztt/Scene-Implementation/models"
	MQTT "github.com/eclipse/paho.mqtt.golang"
)

func OnConnect(client MQTT.Client) {
	fmt.Println("Relay server successfully connected to broker")
}

func OnPresence(client MQTT.Client, message MQTT.Message) {
	fmt.Println("Simulation now online")
	simulationConnected = true
}

func OnContConnect(client MQTT.Client, message MQTT.Message) {
	// var msg string = message.Topic()
	// var msgSliced []string = strings.Split(msg, "/")
	// var contID string = msgSliced[2]
	// adding to the controllers map with empty device list
	var msg string = string(message.Payload())
	var deviceIDs = strings.Split(msg, ",")

	// add devices to online devices list
	for _, device := range deviceIDs {
		onlineDevices[device] = mem
	}

	/*
		TODO:
			broadcast connected devices to frontend
	*/

	fmt.Printf("Updated list of online devices: %s\n", strings.Join(deviceIDs, ", "))
}

func OnContDisconnect(client MQTT.Client, message MQTT.Message) {
	// var msg string = message.Topic()
	// var msgSliced []string = strings.Split(msg, "/")
	// var contID string = msgSliced[2]

	var msg string = string(message.Payload())
	var deviceIDs = strings.Split(msg, ",")
	// first remove all the devices from online list
	for _, device := range deviceIDs {
		delete(onlineDevices, device)
	}

	/*
		TODO:
			broadcast disconnected devices to frontend
			save device state to database before deleting from maps
	*/

	// do this only when device is deleted
	// for _, device := range deviceIDs {
	// 	if _, ok := acs[device]; ok {
	// 		delete(acs, device)
	// 	} else if _, ok := colorLights[device]; ok {
	// 		delete(acs, device)
	// 	} else if _, ok := doorLocks[device]; ok {
	// 		delete(acs, device)
	// 	} else if _, ok := fans[device]; ok {
	// 		delete(acs, device)
	// 	} else if _, ok := lights[device]; ok {
	// 		delete(acs, device)
	// 	}
	// }
	var newDevices []string = make([]string, 0, len(onlineDevices))
	for device := range onlineDevices {
		newDevices = append(newDevices, device)
	}
	fmt.Printf("Updated list of online devices: %s\n", strings.Join(newDevices, ", "))
}

func OnWill(client MQTT.Client, message MQTT.Message) {
	fmt.Printf("Some devices disconnected unexpectedly")
	OnContDisconnect(client, message)
}

func OnDeviceStatus(client MQTT.Client, message MQTT.Message) {
	var msg string = message.Topic()
	var msgSliced []string = strings.Split(msg, "/")
	var deviceType string = msgSliced[2]

	/*
		TODO:
			add websocket post to the frontend
	*/

	var did string
	var status string

	var ac MODELS.AC
	var clight MODELS.ColorLight
	var dlock MODELS.DoorLock
	var fan MODELS.Fan
	var light MODELS.Light

	if deviceType == MODELS.AC_TYPE {
		json.Unmarshal(message.Payload(), &ac)

		// add device to device list if not already present
		if _, ok := acs[ac.ID]; !ok {
			acs[ac.ID] = ac
		}
		did = ac.ID
		status = ac.GetStatusString()
	} else if deviceType == MODELS.CLIGHT_TYPE {
		json.Unmarshal(message.Payload(), &clight)

		// add device to device list if not already present
		if _, ok := acs[clight.ID]; !ok {
			colorLights[clight.ID] = clight
		}
		did = clight.ID
		status = clight.GetStatusString()
	} else if deviceType == MODELS.DLOCK_TYPE {
		json.Unmarshal(message.Payload(), &dlock)

		// add device to device list if not already present
		if _, ok := acs[dlock.ID]; !ok {
			doorLocks[dlock.ID] = dlock
		}
		did = dlock.ID
		status = dlock.GetStatusString()
	} else if deviceType == MODELS.FAN_TYPE {
		json.Unmarshal(message.Payload(), &fan)

		// add device to device list if not already present
		if _, ok := acs[fan.ID]; !ok {
			fans[fan.ID] = fan
		}
		did = fan.ID
		status = fan.GetStatusString()
	} else if deviceType == MODELS.LIGHT_TYPE {
		json.Unmarshal(message.Payload(), &light)

		// add device to device list if not already present
		if _, ok := acs[light.ID]; !ok {
			lights[light.ID] = light
		}
		did = light.ID
		status = light.GetStatusString()
	}

	// updating to db
	err := DB.UpdateDeviceStatus(did, status)
	if err != nil {
		fmt.Println("Could not update db. not sending to client")
	} else {
		// websocket broadcast here
	}

}
