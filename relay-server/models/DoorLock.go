package models

import (
	"fmt"
	"strings"
)

type DoorLock struct {
	ID    string
	Name  string
	Type  string
	State string
}

func (dlock DoorLock) GetParamString() string {
	var params string = ""

	return params
}

func (dlock DoorLock) GetStatusString() string {
	var status string = fmt.Sprintf(
		"state:%s",
		dlock.State,
	)
	return status
}

func (dlock *DoorLock) SetFromStatusString(status string) {
	var params []string = strings.Split(status, "|")

	dlock.State = strings.Split(params[0], ":")[1]
}
