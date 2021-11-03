package database

import (
	"fmt"

	MODELS "github.com/azztt/Scene-Implementation/models"
)

// get all scenes
func GetAllScenes() ([]MODELS.Scene, error) {
	var scenes []MODELS.Scene

	rows, err := db.Query(fmt.Sprintf("SELECT * FROM %s", SCENE_TABLE))

	if err != nil {
		return nil, fmt.Errorf("GetAllScenes: %v", err)
	}

	defer rows.Close()

	for rows.Next() {
		var scene MODELS.Scene
		err = rows.Scan(&scene.ID, &scene.Name)
		if err != nil {
			return nil, fmt.Errorf("GetAllScenes: %v", err)
		}
		scenes = append(scenes, scene)
	}
	return scenes, nil
}

// get scene details from database
func GetSceneByID(sceneId int64) (MODELS.Scene, error) {
	sceneRow := db.QueryRow(
		fmt.Sprintf("SELECT * FROM %s WHERE id = ?", SCENE_TABLE),
		sceneId,
	)

	var scene MODELS.Scene

	err := sceneRow.Scan(
		&scene.ID,
		&scene.Name,
	)
	if err != nil {
		return scene, fmt.Errorf("GetSceneByID: %v", err)
	}

	return scene, nil
}

// save new scene
func InsertNewScene(scene MODELS.Scene) (int64, error) {
	cmd, _ := db.Prepare(
		fmt.Sprintf("INSERT INTO %s (name) VALUES (?)", SCENE_TABLE),
	)

	res, err := cmd.Exec(
		scene.Name,
	)
	if err != nil {
		return 0, fmt.Errorf("InsertNewScene: %v", err)
	}
	newId, err := res.LastInsertId()
	if err != nil {
		return 0, fmt.Errorf("InsertNewScene: %v", err)
	}
	return newId, nil
}

// delete scene by id
func DeleteSceneById(sceneId int64) error {
	cmd, _ := db.Prepare(
		fmt.Sprintf("DELETE FROM %s WHERE id = ?", SCENE_TABLE),
	)
	_, err := cmd.Exec(
		sceneId,
	)
	if err != nil {
		return fmt.Errorf("DeleteSceneById: %v", err)
	}
	return nil
}
