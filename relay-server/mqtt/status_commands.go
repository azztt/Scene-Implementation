package mqtt

import (
	"fmt"
	"strings"

	CONFIG "github.com/azztt/Scene-Implementation/config"
	DB "github.com/azztt/Scene-Implementation/database"
	MODELS "github.com/azztt/Scene-Implementation/models"
	MQTT "github.com/eclipse/paho.mqtt.golang"
)

func SetDeviceStatusAck(client MQTT.Client, message MQTT.Message) error {
	// first unsubscribe from the topic
	client.Unsubscribe(message.Topic())
	var status string = strings.Split(string(message.Payload()), "/")[1]

	if status == "FAILED" {
		return fmt.Errorf("FAILED status from device command")
	}
	return nil
}

func SetScene(sceneId int64) error {
	// first get scene configs from database
	var sceneConfigs []MODELS.Config
	var err error
	done := 0
	sceneConfigs, err = DB.GetConfigsBySceneID(sceneId)
	if err != nil {
		fmt.Println("Could not fetch scene data. Aborting")
		return err
	}

	for _, config := range sceneConfigs {
		client.Subscribe(
			CONFIG.GetDeviceAckTopic(config.DeviceId),
			byte(CONFIG.MQTT_QOS),
			func(c MQTT.Client, m MQTT.Message) {
				err = SetDeviceStatusAck(c, m)
				done += 1
			},
		)

		client.Publish(
			CONFIG.GetDeviceComTopic(config.DeviceId),
			byte(CONFIG.MQTT_QOS),
			false,
			config.DeviceConfig,
		)
	}

	for {
		if done == len(sceneConfigs) {
			break
		}
	}
	if err != nil {
		return err
	}
	return nil
}
