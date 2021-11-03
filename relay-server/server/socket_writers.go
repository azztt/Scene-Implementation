package server

import (
	DB "github.com/azztt/Scene-Implementation/database"
	MODELS "github.com/azztt/Scene-Implementation/models"
	MQTT "github.com/azztt/Scene-Implementation/mqtt"
	"github.com/gorilla/websocket"
)

func writeResponse(conn *websocket.Conn, response map[string]interface{}) {
	lock.Lock()
	conn.WriteJSON(response)
	lock.Unlock()
}

func writeErrorResponse(conn *websocket.Conn, req string, err error) {
	response := map[string]interface{}{
		"res":     req,
		"message": "FAILED",
		"error":   err.Error(),
	}
	writeResponse(conn, response)
}

func sendDeviceStatus(conn *websocket.Conn, statusChannel chan map[string]interface{}) {
	for {
		// on getting updated device status
		deviceStatuses := <-statusChannel
		// send updated data to frontend
		writeResponse(conn, deviceStatuses)
	}
}

func getEverything(conn *websocket.Conn, req string) {
	var data map[string]interface{} = map[string]interface{}{}
	var err error

	// wasError := false

	// get rooms
	var rooms []MODELS.Room
	rooms, err = DB.GetAllRooms()
	if err != nil {
		writeErrorResponse(conn, req, err)
		return
	}

	// get devices
	var devices []MODELS.Device
	devices, err = DB.GetAllDevices()
	if err != nil {
		writeErrorResponse(conn, req, err)
		return
	}

	// get scenes
	var scenes []MODELS.Scene
	scenes, err = DB.GetAllScenes()
	if err != nil {
		writeErrorResponse(conn, req, err)
		return
	}

	// get configs
	var configs []MODELS.Config
	configs, err = DB.GetAllConfigs()
	if err != nil {
		writeErrorResponse(conn, req, err)
		return
	}

	var response map[string]interface{}

	// if wasError {
	// 	writeErrorResponse(conn, req, err)
	// 	return
	// } else {
	data["rooms"] = rooms
	data["devices"] = devices
	data["scenes"] = scenes
	data["configs"] = configs

	response = map[string]interface{}{
		"res":     req,
		"message": "DEVICE_STATUS",
		"data":    data,
	}
	// }
	writeResponse(conn, response)
}

func createScene(conn *websocket.Conn, req string, body map[string]interface{}) {
	var newSceneId int64
	var err error
	var newSceneName = body["name"].(string)
	var deviceConfigs []map[string]interface{} = body["deviceConfigs"].([]map[string]interface{})
	// create new scene in db
	newSceneId, err = DB.InsertNewScene(MODELS.Scene{
		Name: newSceneName,
	})
	if err != nil {
		writeErrorResponse(conn, req, err)
		return
	}
	var newScene MODELS.Scene = MODELS.Scene{
		ID:   newSceneId,
		Name: newSceneName,
	}
	// write the device configs to db
	err = DB.InsertNewConfigs(newSceneId, deviceConfigs)
	if err != nil {
		writeErrorResponse(conn, req, err)
		return
	}
	var newConfigs []MODELS.Config = make([]MODELS.Config, 0, 10)
	for _, deviceConfig := range deviceConfigs {
		config := MODELS.Config{
			DeviceId:     deviceConfig["deviceId"].(string),
			SceneId:      newSceneId,
			DeviceConfig: deviceConfig["config"].(string),
		}
		newConfigs = append(newConfigs, config)
	}
	response := map[string]interface{}{
		"res":     req,
		"message": "SUCCESS",
		"data": map[string]interface{}{
			"scene":   newScene,
			"configs": newConfigs,
		},
	}
	writeResponse(conn, response)
}

func editScene(conn *websocket.Conn, req string, body map[string]interface{}) {
	var sceneId int64 = body["sceneId"].(int64)
	var err error
	var deviceConfigs []map[string]interface{} = body["deviceConfigs"].([]map[string]interface{})

	// write the new device configs to db
	err = DB.UpdateConfigs(sceneId, deviceConfigs)
	if err != nil {
		writeErrorResponse(conn, req, err)
		return
	}
	var newConfigs []MODELS.Config = make([]MODELS.Config, 0, 10)
	for _, deviceConfig := range deviceConfigs {
		config := MODELS.Config{
			DeviceId:     deviceConfig["deviceId"].(string),
			SceneId:      sceneId,
			DeviceConfig: deviceConfig["config"].(string),
		}
		newConfigs = append(newConfigs, config)
	}
	response := map[string]interface{}{
		"res":     req,
		"message": "SUCCESS",
		"data": map[string]interface{}{
			"configs": newConfigs,
		},
	}
	writeResponse(conn, response)
}

func deleteScene(conn *websocket.Conn, req string, body map[string]interface{}) {
	delSceneId := body["sceneId"].(int64)
	err := DB.DeleteSceneById(delSceneId)
	if err != nil {
		writeErrorResponse(conn, req, err)
		return
	}
	response := map[string]interface{}{
		"res":     req,
		"message": "SUCCESS",
	}
	writeResponse(conn, response)
}

func createRoom(conn *websocket.Conn, req string, body map[string]interface{}) {
	newRoomName := body["name"].(string)
	// adding to simulation
	room, err := MQTT.NewRoom(newRoomName)

	if err != nil {
		writeErrorResponse(conn, req, err)
		return
	}

	response := map[string]interface{}{
		"res":     req,
		"message": "SUCCESS",
		"data": map[string]interface{}{
			"room": room,
		},
	}
	writeResponse(conn, response)
}

func deleteRoom(conn *websocket.Conn, req string, body map[string]interface{}) {
	delRoomId := body["roomId"].(string)

	// deleting from simulation
	err := MQTT.RemoveRoom(delRoomId)
	if err != nil {
		writeErrorResponse(conn, req, err)
		return
	}

	response := map[string]interface{}{
		"res":     req,
		"message": "SUCCESS",
	}
	writeResponse(conn, response)
}

func createDevice(conn *websocket.Conn, req string, body map[string]interface{}) {
	deviceParams := body

	var device MODELS.Device
	var err error

	device, err = MQTT.NewDevice(deviceParams)

	if err != nil {
		writeErrorResponse(conn, req, err)
	}
	response := map[string]interface{}{
		"res":     req,
		"message": "SUCCESS",
		"data": map[string]interface{}{
			"device": device,
		},
	}
	writeResponse(conn, response)
}

func deleteDevice(conn *websocket.Conn, req string, body map[string]interface{}) {
	delDeviceId := body["deviceId"].(string)

	// deleting from simulation
	err := MQTT.RemoveRoom(delDeviceId)
	if err != nil {
		writeErrorResponse(conn, req, err)
		return
	}

	response := map[string]interface{}{
		"res":     req,
		"message": "SUCCESS",
	}
	writeResponse(conn, response)
}

func setScene(conn *websocket.Conn, req string, body map[string]interface{}) {
	sceneId := body["sceneId"].(int64)
	err := MQTT.SetScene(sceneId)
	if err != nil {
		writeErrorResponse(conn, req, err)
		return
	}
	response := map[string]interface{}{
		"res":     req,
		"message": "SUCCESS",
	}
	writeResponse(conn, response)
}
