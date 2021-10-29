package database

import (
	"fmt"
	MODELS "github.com/azztt/Scene-Implementation/models"
)

// get all device rows from DB
func GetAllDevices() ([]MODELS.Device, error) {
	var deviceData []MODELS.Device = make([]MODELS.Device, 0, 10)

	rows, err := db.Query(
		"SELECT * FROM ?",
		DEVICE_TABLE,
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
func UpdateDeviceStatus(deviceId string, status string) error {
	cmd, _ := db.Prepare(
		"UPDATE ? SET status = ? WHERE id = ?",
	)
	_, err := cmd.Exec(DEVICE_TABLE, status, deviceId)
	if err != nil {
		return fmt.Errorf("UpdateDeviceStatus: %v", err)
	}
	return nil
}

// insert new device
func InsertNewDevice(device MODELS.Device) error {
	cmd, _ := db.Prepare(
		"INSERT INTO ? (id, name, parameters, status, type) VALUES (?, ?, ?, ?)",
	)

	_, err := cmd.Exec(
		DEVICE_TABLE,
		device.ID,
		device.Name,
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
		"DELETE FROM ? WHERE id = ?",
	)
	_, err := cmd.Exec(
		DEVICE_TABLE,
		deviceId,
	)
	if err != nil {
		return fmt.Errorf("DeleteDeviceById: %v", err)
	}
	return nil
}
