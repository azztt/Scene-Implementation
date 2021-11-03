package database

import (
	"fmt"

	MODELS "github.com/azztt/Scene-Implementation/models"
)

// get all rooms
func GetAllRooms() ([]MODELS.Room, error) {
	var rooms []MODELS.Room

	rows, err := db.Query(fmt.Sprintf("SELECT * FROM %s", ROOM_TABLE))

	if err != nil {
		return nil, fmt.Errorf("GetAllRooms: %v", err)
	}

	defer rows.Close()

	for rows.Next() {
		var room MODELS.Room
		err = rows.Scan(&room.ID, &room.Name)
		if err != nil {
			return nil, fmt.Errorf("GetAllRooms: %v", err)
		}
		rooms = append(rooms, room)
	}
	return rooms, nil
}

// get room details from database
func GetRoomByID(roomId string) (MODELS.Room, error) {
	roomRow := db.QueryRow(
		fmt.Sprintf("SELECT * FROM %s WHERE id = ? LIMIT 1", ROOM_TABLE),
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

// insert new room
func InsertNewRoom(room MODELS.Room) error {
	cmd, _ := db.Prepare(
		fmt.Sprintf("INSERT INTO %s (id, name) VALUES (?, ?)", ROOM_TABLE),
	)

	_, err := cmd.Exec(
		room.ID,
		room.Name,
	)
	if err != nil {
		return fmt.Errorf("InsertNewRoom: %v", err)
	}
	return nil
}

// delete room by id
func DeleteRoomById(roomId string) error {
	cmd, _ := db.Prepare(
		fmt.Sprintf("DELETE FROM %s WHERE id = ?", ROOM_TABLE),
	)
	_, err := cmd.Exec(
		roomId,
	)
	if err != nil {
		return fmt.Errorf("DeleteRoomById: %v", err)
	}
	return nil
}
