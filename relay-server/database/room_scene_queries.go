package database

import (
	"fmt"

	MODELS "github.com/azztt/Scene-Implementation/models"
)

// get pair details from database
func GetPairByID(roomId string) (MODELS.Room, error) {
	roomRow := db.QueryRow(
		"SELECT * FROM ? WHERE id = ? LIMIT 1",
		ROOM_TABLE,
		roomId,
	)

	var room MODELS.Room

	err := roomRow.Scan(
		&room.ID,
		&room.Name,
	)
	if err != nil {
		return room, fmt.Errorf("GetRoomByID: %v", err)
	}

	return room, nil
}

// insert new pair
func InsertNewPair(pair MODELS.RoomScene) (int64, error) {
	cmd, _ := db.Prepare(
		"INSERT INTO ? (sceneId, roomId) VALUES (?, ?)",
	)

	res, err := cmd.Exec(
		ROOM_SCENE_TABLE,
		pair.SceneId,
		pair.RoomId,
	)
	if err != nil {
		return 0, fmt.Errorf("InsertNewPair: %v", err)
	}
	newId, err := res.LastInsertId()
	if err != nil {
		return 0, fmt.Errorf("InsertNewPair: %v", err)
	}
	return newId, nil
}

// delete pair by room id
func DeletePairByRoomId(roomId string) error {
	cmd, _ := db.Prepare(
		"DELETE FROM ? WHERE roomId = ?",
	)
	_, err := cmd.Exec(
		ROOM_SCENE_TABLE,
		roomId,
	)
	if err != nil {
		return fmt.Errorf("DeletePairByRoomId: %v", err)
	}
	return nil
}

// delete pair by room id
func DeletePairBySceneId(sceneId string) error {
	cmd, _ := db.Prepare(
		"DELETE FROM ? WHERE sceneId = ?",
	)
	_, err := cmd.Exec(
		ROOM_SCENE_TABLE,
		sceneId,
	)
	if err != nil {
		return fmt.Errorf("DeletePairBySceneId: %v", err)
	}
	return nil
}
