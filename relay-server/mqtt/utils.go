package mqtt

import (
	"fmt"
)

func structToStatusString(status map[string]interface{}) string {
	var statusString string = ""

	if _, ok := status["temperature"]; ok {
		statusString += fmt.Sprintf("power:%v|", status["power"])
		statusString += fmt.Sprintf("temperature:%v|", status["temperature"])
		statusString += fmt.Sprintf("fanSpeed:%v|", status["fanSpeed"])
		statusString += fmt.Sprintf("swingState:%v|", status["swingState"])
		statusString += fmt.Sprintf("mode:%v", status["mode"])
	} else if _, ok := status["color"]; ok {
		statusString += fmt.Sprintf("power:%v|", status["power"])
		statusString += fmt.Sprintf("brightness:%v|", status["brightness"])
		statusString += fmt.Sprintf("color:%v", status["color"])
	} else if _, ok := status["status"]; ok {
		statusString += fmt.Sprintf("power:%v|", status["power"])
		statusString += fmt.Sprintf("status:%v", status["status"])
	} else if _, ok := status["speed"]; ok {
		statusString += fmt.Sprintf("power:%v|", status["power"])
		statusString += fmt.Sprintf("speed:%v", status["speed"])
	} else if _, ok := status["brightness"]; ok {
		statusString += fmt.Sprintf("power:%v|", status["power"])
		statusString += fmt.Sprintf("brightness:%v", status["brightness"])
	}

	// for key, value := range status {
	// 	statusString += fmt.Sprintf("%s:%v|", key, value)
	// }

	// statusString = statusString[:len(statusString)-1]
	return statusString
}

func sliceContains(values []string, value string) bool {
	for _, val := range values {
		if val == value {
			return true
		}
	}
	return false
}
