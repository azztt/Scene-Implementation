package mqtt

import (
	"fmt"
	"strings"

	CONFIG "github.com/azztt/Scene-Implementation/config"
	DB "github.com/azztt/Scene-Implementation/database"
	MODELS "github.com/azztt/Scene-Implementation/models"
	MQTT "github.com/eclipse/paho.mqtt.golang"
)

func SetDeviceStatusAck(client MQTT.Client, message MQTT.Message) {
	// first unsubscribe from the topic
	client.Unsubscribe(message.Topic())
	var status string = strings.Split(string(message.Payload()), "/")[1]

	if status == "FAILED" {
		fmt.Println("FAILED status from device command")
	}
}

func SetScene(sceneId string) {
	// first get scene information from database
	var sceneInfo MODELS.Scene
	var err error
	sceneInfo, err = DB.GetSceneByID(sceneId)
	if err != nil {
		fmt.Println("Could not fetch scene data. Aborting")
		/*
			TODO:
				broadcast to frontend
		*/
		return
	}

	// getting devices already in room
	var roomInfo MODELS.Room
	roomInfo, err = DB.GetRoomByID(sceneInfo.RoomId)

	if err != nil {
		fmt.Println("Could not fetch scene data. Aborting")
		/*
			TODO:
				broadcast to frontend
		*/
		return
	}
	var roomDevices []string = roomInfo.DeviceIds

	var deviceIds []string = strings.Split(sceneInfo.DeviceIds, ",")
	var deviceConfigs []string = strings.Split(sceneInfo.DeviceConfigs, "||")

	for in, deviceId := range deviceIds {
		client.Subscribe(
			CONFIG.GetDeviceAckTopic(deviceId),
			byte(CONFIG.MQTT_QOS),
			SetDeviceStatusAck,
		)

		client.Publish(
			CONFIG.GetDeviceComTopic(deviceId),
			byte(CONFIG.MQTT_QOS),
			false,
			deviceConfigs[in],
		)
	}

	// power off all other devices in the room
	for _, deviceId := range roomDevices {
		if !sliceContains(deviceIds, deviceId) {
			// power off this device
			client.Subscribe(
				CONFIG.GetDeviceAckTopic(deviceId),
				byte(CONFIG.MQTT_QOS),
				SetDeviceStatusAck,
			)

			client.Publish(
				CONFIG.GetDeviceComTopic(deviceId),
				byte(CONFIG.MQTT_QOS),
				false,
				deviceId+" "+"OFF",
			)
		}
	}

	/*
		TODO:
			broadcast to frontend
	*/
}
