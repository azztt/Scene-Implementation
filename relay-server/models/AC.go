package models

import (
	"fmt"
	"strconv"
	"strings"
)

type AC struct {
	ID          string
	Name        string
	Type        string
	TempRange   string
	CurrentTemp int
	FanSpeed    string
	SwingState  string
	Mode        string
}

func (ac *AC) CreateDevice(device map[string]interface{}) {
	ac.ID = device["id"].(string)
	ac.Name = device["name"].(string)
	ac.Type = device["type"].(string)
	ac.TempRange = device["temp_range"].(string)
}

func (ac AC) GetParamString() string {
	var params string = fmt.Sprintf(
		"tempRange:%s",
		ac.TempRange,
	)

	return params
}

func (ac *AC) SetFromParamString(param string) {
	var params []string = strings.Split(param, "|")
	var tempRange string = strings.Split(params[0], ":")[1]
	ac.TempRange = tempRange
}

func (ac AC) GetStatusString() string {
	var status string = fmt.Sprintf(
		"currentTemp:%d|fanSpeed:%s|swingState:%s|mode:%s",
		ac.CurrentTemp,
		ac.FanSpeed,
		ac.SwingState,
		ac.Mode,
	)
	return status
}

func (ac *AC) SetStatusFromString(status string) {
	var params []string = strings.Split(status, "|")

	temp, _ := strconv.Atoi(strings.Split(params[0], ":")[1])
	ac.CurrentTemp = temp

	ac.FanSpeed = strings.Split(params[1], ":")[1]

	ac.SwingState = strings.Split(params[2], ":")[1]

	ac.Mode = strings.Split(params[3], ":")[1]
}
