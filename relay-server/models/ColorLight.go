package models

import (
	"fmt"
	"strconv"
	"strings"
)

type ColorLight struct {
	ID           string
	Name         string
	Type         string
	BrightLevels int
	Brightness   int
	Color        string
}

func (clight *ColorLight) CreateDevice(device map[string]interface{}) {
	clight.ID = device["id"].(string)
	clight.Name = device["name"].(string)
	clight.Type = device["type"].(string)
	clight.BrightLevels, _ = strconv.Atoi(device["b_levels"].(string))
}

func (clight ColorLight) GetParamString() string {
	var params string = fmt.Sprintf(
		"brightLevels:%d",
		clight.BrightLevels,
	)

	return params
}

func (clight *ColorLight) SetFromParamString(param string) {
	var params []string = strings.Split(param, "|")
	var brightLevelsS string = strings.Split(params[0], ":")[1]
	var brightLevels int
	brightLevels, _ = strconv.Atoi(brightLevelsS)
	clight.BrightLevels = brightLevels

}

func (clight ColorLight) GetStatusString() string {
	var status string = fmt.Sprintf(
		"brightness:%d|color:%s",
		clight.Brightness,
		clight.Color,
	)
	return status
}

func (clight *ColorLight) SetFromStatusString(status string) {
	var params []string = strings.Split(status, "|")

	brightness, _ := strconv.Atoi(strings.Split(params[0], ":")[1])
	clight.Brightness = brightness

	clight.Color = strings.Split(params[1], ":")[1]
}
