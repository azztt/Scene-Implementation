package database

import (
	"fmt"

	MODELS "github.com/azztt/Scene-Implementation/models"
)

// get all configs
func GetAllConfigs() ([]MODELS.Config, error) {
	var configs []MODELS.Config = make([]MODELS.Config, 0, 10)

	rows, err := db.Query(fmt.Sprintf("SELECT * FROM %s", CONFIG_TABLE))

	if err != nil {
		return nil, fmt.Errorf("GetAllConfigs: %v", err)
	}

	defer rows.Close()

	for rows.Next() {
		var config MODELS.Config
		err = rows.Scan(&config.ID, &config.DeviceId, &config.SceneId, &config.DeviceConfig)
		if err != nil {
			return nil, fmt.Errorf("GetAllConfigs: %v", err)
		}
		configs = append(configs, config)
	}
	return configs, nil
}

// get all configs for a selected scene
func GetConfigsBySceneID(sceneId int64) ([]MODELS.Config, error) {
	var configs []MODELS.Config = make([]MODELS.Config, 0, 10)

	rows, err := db.Query(
		fmt.Sprintf("SELECT deviceId, deviceConfig FROM %s WHERE sceneId = ?", CONFIG_TABLE),
		sceneId,
	)

	if err != nil {
		return configs, fmt.Errorf("GetConfigsBySceneID: %v", err)
	}
	defer rows.Close()

	for rows.Next() {
		var config MODELS.Config
		err := rows.Scan(
			&config.DeviceId,
			&config.DeviceConfig,
		)
		if err != nil {
			return nil, fmt.Errorf("GetConfigsBySceneID: %v", err)
		}
		configs = append(configs, config)
	}

	return configs, nil
}

// insert new configs
func InsertNewConfigs(sceneId int64, configs []interface{}) error {
	var sqlCmd string = fmt.Sprintf("INSERT INTO %s (deviceId, sceneId, deviceConfig) VALUES ", CONFIG_TABLE)
	var vals []interface{}
	for _, config := range configs {
		sqlCmd += "(?, ?, ?),"
		vals = append(vals, config.(map[string]interface{})["deviceId"].(string), sceneId, config.(map[string]interface{})["config"].(string))
	}
	sqlCmd = sqlCmd[0 : len(sqlCmd)-1]
	cmd, _ := db.Prepare(sqlCmd)

	_, err := cmd.Exec(vals...)
	if err != nil {
		return fmt.Errorf("InsertNewConfigs: %v", err)
	}
	return nil
}

func UpdateConfigs(sceneId int64, configs []map[string]interface{}) error {
	var err error
	for _, config := range configs {
		cmd, _ := db.Prepare(
			fmt.Sprintf("UPDATE %s SET deviceConfig = ? WHERE sceneId = ? AND deviceId = ?", CONFIG_TABLE),
		)
		_, err = cmd.Exec(config["config"], sceneId, config["deviceId"])
	}
	if err != nil {
		return fmt.Errorf("UpdateDeviceStatus: %v", err)
	}

	return nil
}

// delete config by scene id
func DeleteConfigBySceneId(sceneId string) error {
	cmd, _ := db.Prepare(
		fmt.Sprintf("DELETE FROM %s WHERE sceneId = ?", CONFIG_TABLE),
	)
	_, err := cmd.Exec(
		sceneId,
	)
	if err != nil {
		return fmt.Errorf("DeleteConfigBySceneId: %v", err)
	}
	return nil
}

// delete config by device id
func DeleteConfigByDeviceId(deviceId string) error {
	cmd, _ := db.Prepare(
		fmt.Sprintf("DELETE FROM %s WHERE deviceId = ?", CONFIG_TABLE),
	)
	_, err := cmd.Exec(
		deviceId,
	)
	if err != nil {
		return fmt.Errorf("DeleteConfigByDeviceId: %v", err)
	}
	return nil
}

// delete config by device ids with room id
func DeleteDeviceConfigByRoomId(roomId string) error {
	cmd, _ := db.Prepare(
		fmt.Sprintf("DELETE FROM %s WHERE deviceId IN (SELECT (id) FROM ? WHERE roomID = ?)", CONFIG_TABLE),
	)
	_, err := cmd.Exec(
		DEVICE_TABLE,
		roomId,
	)
	if err != nil {
		return fmt.Errorf("DeleteConfigByRoomId: %v", err)
	}
	return nil
}
