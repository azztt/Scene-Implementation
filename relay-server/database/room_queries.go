package database

import (
	"fmt"
	"strings"

	MODELS "github.com/azztt/Scene-Implementation/models"
)

// get room details from database
func GetRoomByID(roomId string) (MODELS.Room, error) {
	roomRow := db.QueryRow(
		"SELECT * FROM ? WHERE id = ? LIMIT 1",
		ROOM_TABLE,
		roomId,
	)

	var room MODELS.Room

	var deviceIds string

	err := roomRow.Scan(
		&room.ID,
		&room.Name,
		&deviceIds,
	)
	room.DeviceIds = strings.Split(deviceIds, ",")
	if err != nil {
		return room, fmt.Errorf("GetRoomByID: %v", err)
	}

	return room, nil
}

// insert new room
func InsertNewRoom(room MODELS.Room) error {
	cmd, _ := db.Prepare(
		"INSERT INTO ? (id, name, deviceIds) VALUES (?, ?, ?)",
	)

	_, err := cmd.Exec(
		ROOM_TABLE,
		room.ID,
		room.Name,
		strings.Join(room.DeviceIds, ","),
	)
	if err != nil {
		return fmt.Errorf("InsertNewRoom: %v", err)
	}
	return nil
}

// delete room by id
func DeleteRoomById(roomId string) error {
	cmd, _ := db.Prepare(
		"DELETE FROM ? WHERE id = ?",
	)
	_, err := cmd.Exec(
		ROOM_TABLE,
		roomId,
	)
	if err != nil {
		return fmt.Errorf("DeleteRoomById: %v", err)
	}
	return nil
}
