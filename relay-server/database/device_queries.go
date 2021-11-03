package database

import (
	"fmt"

	MODELS "github.com/azztt/Scene-Implementation/models"
)

// get all device rows from DB
func GetAllDevices() ([]MODELS.Device, error) {
	var deviceData []MODELS.Device = make([]MODELS.Device, 0, 10)

	rows, err := db.Query(
		fmt.Sprintf("SELECT * FROM %s", DEVICE_TABLE),
	)

	if err != nil {
		return nil, fmt.Errorf("GetAllDevices: %v", err)
	}
	defer rows.Close()

	for rows.Next() {
		var data MODELS.Device
		err := rows.Scan(
			&data.ID,
			&data.Name,
			&data.RoomId,
			&data.Parameters,
			&data.Status,
			&data.Type,
		)
		if err != nil {
			return nil, fmt.Errorf("GetAllDevices: %v", err)
		}
		deviceData = append(deviceData, data)
	}

	return deviceData, nil
}

// write device status
func UpdateDeviceStatus(deviceId string, status string) (int64, error) {
	cmd, _ := db.Prepare(
		fmt.Sprintf("UPDATE %s SET status = ? WHERE id = ?", DEVICE_TABLE),
	)
	res, err := cmd.Exec(status, deviceId)
	if err != nil {
		return 0, fmt.Errorf("UpdateDeviceStatus: %v", err)
	}
	affectedRows, _ := res.RowsAffected()
	return affectedRows, nil
}

// insert new device
func InsertNewDevice(device MODELS.Device) error {
	cmd, _ := db.Prepare(
		fmt.Sprintf("INSERT INTO %s (id, name, roomId, parameters, status, type) VALUES (?, ?, ?, ?, ?)", DEVICE_TABLE),
	)

	_, err := cmd.Exec(
		device.ID,
		device.Name,
		device.RoomId,
		device.Parameters,
		device.Status,
		device.Type,
	)
	if err != nil {
		return fmt.Errorf("InsertNewDevice: %v", err)
	}
	return nil
}

// delete device by id
func DeleteDeviceById(deviceId string) error {
	cmd, _ := db.Prepare(
		fmt.Sprintf("DELETE FROM %s WHERE id = ?", DEVICE_TABLE),
	)
	_, err := cmd.Exec(
		deviceId,
	)
	if err != nil {
		return fmt.Errorf("DeleteDeviceById: %v", err)
	}
	return nil
}

// delete device by id
func DeleteDeviceByRoomId(roomId string) error {
	cmd, _ := db.Prepare(
		fmt.Sprintf("DELETE FROM %s WHERE roomId = ?", DEVICE_TABLE),
	)
	_, err := cmd.Exec(
		DEVICE_TABLE,
		roomId,
	)
	if err != nil {
		return fmt.Errorf("DeleteDeviceByRoomId: %v", err)
	}
	return nil
}

// get device id
