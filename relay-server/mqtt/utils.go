package mqtt

import "fmt"

func structToStatusString(status map[string]interface{}) string {
	var statusString string = ""

	for key, value := range status {
		statusString += fmt.Sprintf("%s:%v|", key, value)
	}

	statusString = statusString[:len(statusString)-1]
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
