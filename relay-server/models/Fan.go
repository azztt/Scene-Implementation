package models

import (
	"fmt"
	"strconv"
	"strings"
)

type Fan struct {
	ID                string
	Name              string
	Type              string
	SpeedLevels       int
	CurrentSpeedLevel int
}

func (fan *Fan) CreateDevice(device map[string]interface{}) {
	fan.ID = device["id"].(string)
	fan.Name = device["name"].(string)
	fan.Type = device["type"].(string)
	fan.SpeedLevels, _ = strconv.Atoi(device["speed_levels"].(string))
}

func (fan Fan) GetParamString() string {
	var params string = fmt.Sprintf(
		"speedLevels:%d",
		fan.SpeedLevels,
	)

	return params
}

func (fan *Fan) SetFromParamString(param string) {
	var params []string = strings.Split(param, "|")
	var speedLevelsS string = strings.Split(params[0], ":")[1]
	var speedLevels int
	speedLevels, _ = strconv.Atoi(speedLevelsS)
	fan.SpeedLevels = speedLevels
}

func (fan Fan) GetStatusString() string {
	var status string = fmt.Sprintf(
		"currentSpeedLevel:%d",
		fan.CurrentSpeedLevel,
	)
	return status
}

func (fan *Fan) SetStatusFromString(status string) {
	var params []string = strings.Split(status, "|")

	speed, _ := strconv.Atoi(strings.Split(params[0], ":")[1])
	fan.CurrentSpeedLevel = speed
}
