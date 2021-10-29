package config

type command string

const (
	DEVICE_OFF command = "OFF"
	DEVICE_ON  command = "ON"

	FAN_SET_SPEED command = "set_speed"

	AC_SET_TEMP      command = "set_temp"
	AC_SET_FAN_SPEED command = "set_fan_speed"
	AC_SET_SWING     command = "set_swing"
	AC_SET_MODE      command = "set_mode"

	L_SET_BRIGHT command = "set_brightness"
	L_SET_COLOR  command = "set_color"

	DL_SET_LOCK command = "set_lock"
)
