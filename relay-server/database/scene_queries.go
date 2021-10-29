package database

import (
	"fmt"

	MODELS "github.com/azztt/Scene-Implementation/models"
)

// get scene details from database
func GetSceneByID(sceneId string) (MODELS.Scene, error) {
	sceneRow := db.QueryRow(
		"SELECT * FROM ? WHERE id = ? LIMIT 1",
		SCENE_TABLE,
		sceneId,
	)

	var scene MODELS.Scene

	err := sceneRow.Scan(
		&scene.ID,
		&scene.Name,
		&scene.RoomId,
		&scene.DeviceIds,
		&scene.DeviceConfigs,
	)
	if err != nil {
		return scene, fmt.Errorf("GetSceneByID: %v", err)
	}

	return scene, nil
}

// save new scene
func InsertNewScene(scene MODELS.Scene) error {
	cmd, _ := db.Prepare(
		"INSERT INTO ? (id, name, roomId, deviceIds, deviceConfigs) VALUES (?, ?, ?, ?, ?)",
	)

	_, err := cmd.Exec(
		SCENE_TABLE,
		scene.ID,
		scene.Name,
		scene.RoomId,
		scene.DeviceIds,
		scene.DeviceConfigs,
	)
	if err != nil {
		return fmt.Errorf("InsertNewScene: %v", err)
	}
	return nil
}

// delete scene by id
func DeleteSceneById(sceneId string) error {
	cmd, _ := db.Prepare(
		"DELETE FROM ? WHERE id = ?",
	)
	_, err := cmd.Exec(
		SCENE_TABLE,
		sceneId,
	)
	if err != nil {
		return fmt.Errorf("DeleteSceneById: %v", err)
	}
	return nil
}
