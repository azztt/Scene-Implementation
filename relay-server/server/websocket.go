package server

import (
	"fmt"
	"net/http"
	"sync"

	CONFIG "github.com/azztt/Scene-Implementation/config"
	"github.com/gorilla/websocket"
	"github.com/labstack/echo/v4"
)

// defining an Upgrader
var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	// currently allowing all
	CheckOrigin: func(r *http.Request) bool { return true },
}

type writerLock struct {
	sync.Mutex
}

var lock writerLock

// define a reader which will listen for
// new messages being sent to our WebSocket
// endpoint
func reader(conn *websocket.Conn) {
	for {
		// read in a message
		// messageType, p, err := conn.ReadMessage()
		// if err != nil {
		// 	log.Println(err)
		// 	return
		// }
		var message map[string]interface{} = make(map[string]interface{})

		err := conn.ReadJSON(&message)
		// print out that message for clarity
		// fmt.Println(string(p))

		// var message map[string]interface{}
		// err = json.Unmarshal(p, &message)

		if err != nil {
			fmt.Println("error in reader: ", err)
			fmt.Println("error parsing message, ignoring and waiting for next")
			continue
		}

		var request string = message["req"].(string)
		var body map[string]interface{}
		if _, ok := message["body"]; ok {
			body = message["body"].(map[string]interface{})
		}

		if request == CONFIG.GET_EVERYTHING {
			go getEverything(conn, request)
		} else if request == CONFIG.CREATE_SCENE {
			go createScene(conn, request, body)
		} else if request == CONFIG.DEL_SCENE {
			go deleteScene(conn, request, body)
		} else if request == CONFIG.CREATE_ROOM {
			go createRoom(conn, request, body)
		} else if request == CONFIG.DEL_ROOM {
			go deleteRoom(conn, request, body)
		} else if request == CONFIG.CREATE_DEVICE {
			go createDevice(conn, request, body)
		} else if request == CONFIG.DEL_DEVICE {
			go deleteDevice(conn, request, body)
		} else if request == CONFIG.SET_SCENE {
			go setScene(conn, request, body)
		} else if request == CONFIG.EDIT_SCENE {
			go editScene(conn, request, body)
		}

		// if err := conn.WriteMessage(messageType, p); err != nil {
		// 	log.Println(err)
		// 	return
		// }

	}
}

var ws *websocket.Conn

// define our WebSocket endpoint
func serveWs(c echo.Context, statusChan chan map[string]interface{}) error {
	// fmt.Println(r.Host)

	// upgrade this connection to a WebSocket
	// connection
	var err error
	ws, err = upgrader.Upgrade(c.Response(), c.Request(), nil)
	if err != nil {
		return err
	}

	// start device status goroutine
	go sendDeviceStatus(ws, statusChan)

	// listen indefinitely for new messages coming
	// through on our WebSocket connection
	reader(ws)
	return nil
}
