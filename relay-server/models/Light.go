package models

import (
	"fmt"
	"strconv"
	"strings"
)

type Light struct {
	ID           string
	Name         string
	Type         string
	BrightLevels int
	Brightness   int
}

func (light *Light) CreateDevice(device map[string]interface{}) {
	light.ID = device["id"].(string)
	light.Name = device["name"].(string)
	light.Type = device["type"].(string)
	light.BrightLevels, _ = strconv.Atoi(device["b_levels"].(string))
}

func (light Light) GetParamString() string {
	var params = fmt.Sprintf(
		"brightLevels:%d",
		light.BrightLevels,
	)

	return params
}

func (light *Light) SetFromParamString(param string) {
	var params []string = strings.Split(param, "|")
	var brightLevelsS string = strings.Split(params[0], ":")[1]
	var brightLevels int
	brightLevels, _ = strconv.Atoi(brightLevelsS)
	light.BrightLevels = brightLevels
}

func (light Light) GetStatusString() string {
	var status string = fmt.Sprintf(
		"brightness:%d",
		light.Brightness,
	)
	return status
}

func (light *Light) SetFromStatusString(status string) {
	var params []string = strings.Split(status, "|")

	brightness, _ := strconv.Atoi(strings.Split(params[0], ":")[1])
	light.Brightness = brightness
}
