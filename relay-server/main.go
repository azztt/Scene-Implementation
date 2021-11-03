package main

import (
	"log"

	DB "github.com/azztt/Scene-Implementation/database"
	MQTT "github.com/azztt/Scene-Implementation/mqtt"
	server "github.com/azztt/Scene-Implementation/server"
)

// main function, execution starts here
func main() {
	var statusChannel chan map[string]interface{} = make(chan map[string]interface{})

	// start database connection
	defer DB.DisconnectDB()
	err := DB.ConnectDB()
	if err != nil {
		log.Fatalf("Error starting db connection: %v", err)
	}
	// start the mqtt client
	defer MQTT.Stop()
	MQTT.Start(statusChannel)

	// start the http and websocket server
	server.StartServer(statusChannel)
}
