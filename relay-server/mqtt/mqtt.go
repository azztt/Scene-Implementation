package mqtt

import (
	"fmt"
	"net/url"
	"os"
	"strconv"

	CONFIG "github.com/azztt/Scene-Implementation/config"
	MODELS "github.com/azztt/Scene-Implementation/models"
	MQTT "github.com/eclipse/paho.mqtt.golang"
)

type void struct{}

var client MQTT.Client

// var simulationConnected bool = false

var acs map[string]MODELS.AC = make(map[string]MODELS.AC)
var colorLights map[string]MODELS.ColorLight = make(map[string]MODELS.ColorLight)
var doorLocks map[string]MODELS.DoorLock = make(map[string]MODELS.DoorLock)
var fans map[string]MODELS.Fan = make(map[string]MODELS.Fan)
var lights map[string]MODELS.Light = make(map[string]MODELS.Light)

// var rooms map[string]MODELS.Room = make(map[string]MODELS.Room)

var mem void
var onlineDevices map[string]void = make(map[string]void)

func Start(statusChannel chan map[string]interface{}) {
	var clientOptions *MQTT.ClientOptions = MQTT.NewClientOptions()
	var brokerURI url.URL = url.URL{
		Scheme: "tcp",
		Host:   CONFIG.MQTT_SERVER + ":" + strconv.Itoa(CONFIG.MQTT_PORT),
	}
	clientOptions.AddBroker(brokerURI.String())
	clientOptions.SetClientID(CONFIG.MQTT_CLIENT_ID)
	clientOptions.SetCleanSession(false)
	clientOptions.SetOnConnectHandler(OnConnect)

	client = MQTT.NewClient(clientOptions)

	// Connect the client
	token := client.Connect()
	if token.Wait() && token.Error() != nil {
		fmt.Printf("Could not connect client")
		os.Exit(1)
	}

	// subscribe to the topics with handlers

	// subscribe to controller presence topic
	token = client.Subscribe(
		CONFIG.PRES_SIM,
		byte(CONFIG.MQTT_QOS),
		OnPresence,
	)
	if token.Wait() && token.Error() != nil {
		fmt.Printf("Could not subscribe to controller presence topic")
		os.Exit(1)
	}

	// subscribe to controller presence topic
	token = client.Subscribe(
		CONFIG.CONT_CON,
		byte(CONFIG.MQTT_QOS),
		OnContConnect,
	)
	if token.Wait() && token.Error() != nil {
		fmt.Printf("Could not subscribe to controller presence topic")
		os.Exit(1)
	}

	// subscribe to controller presence topic
	token = client.Subscribe(
		CONFIG.CONT_DISCON,
		byte(CONFIG.MQTT_QOS),
		OnContDisconnect,
	)
	if token.Wait() && token.Error() != nil {
		fmt.Printf("Could not subscribe to controller disconnection topic")
		os.Exit(1)
	}

	// subscribe to wills
	token = client.Subscribe(
		CONFIG.MQTT_WILL_TOPIC,
		byte(CONFIG.MQTT_QOS),
		OnWill,
	)
	if token.Wait() && token.Error() != nil {
		fmt.Printf("Could not subscribe to controller will topic")
		os.Exit(1)
	}

	// subscribe to cron device statuses
	token = client.Subscribe(
		CONFIG.DEVICE_STATUS,
		byte(CONFIG.MQTT_QOS),
		func(c MQTT.Client, m MQTT.Message) {
			OnDeviceStatus(c, m, statusChannel)
		},
	)
	if token.Wait() && token.Error() != nil {
		fmt.Printf("Could not subscribe to device status")
		os.Exit(1)
	}
}

func Stop() {
	// unsubscribe from all topics subscribed earlier
	client.Unsubscribe(
		CONFIG.PRES_SIM,
		CONFIG.CONT_CON,
		CONFIG.CONT_DISCON,
		CONFIG.MQTT_WILL_TOPIC,
		CONFIG.DEVICE_STATUS,
	)

	// disconnect client
	client.Disconnect(0)
}
