package models

import (
	"fmt"
	"strings"

	"github.com/google/uuid"
)

type Scene struct {
	ID            string
	Name          string
	RoomId        string
	DeviceIds     string
	DeviceConfigs string
}

func (scene *Scene) CreateScene(sceneData map[string]interface{}) {
	uid, _ := uuid.NewRandom()

	scene.ID = uid.String()
	scene.Name = sceneData["name"].(string)
	scene.RoomId = sceneData["roomId"].(string)

	var deviceIds []string = make([]string, 0, 10)
	var deviceConfigs []string = make([]string, 0, 10)

	for key, val := range sceneData["devices"].(map[string]interface{}) {
		deviceIds = append(deviceIds, key)
		var statusString string = ""

		for k, value := range val.(map[string]interface{}) {
			statusString += fmt.Sprintf("%s:%v|", k, value)
		}

		statusString = statusString[:len(statusString)-1]
		deviceConfigs = append(deviceConfigs, statusString)
	}
	scene.DeviceIds = strings.Join(deviceIds, ",")
	scene.DeviceConfigs = strings.Join(deviceConfigs, "||")
}
