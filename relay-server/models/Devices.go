package models

const (
	AC_TYPE     string = "AC"
	CLIGHT_TYPE string = "CLIGHT"
	DLOCK_TYPE  string = "DLOCK"
	FAN_TYPE    string = "FAN"
	LIGHT_TYPE  string = "LIGHT"
)

type Device struct {
	ID         string
	Name       string
	Type       string
	Parameters string
	Status     string
}
