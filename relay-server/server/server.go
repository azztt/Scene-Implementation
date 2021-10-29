package server

import (
	"fmt"
	"net/http"
)

func setupRoutes() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Simple Server")
	})
	// setting up the websocket endpoint
	http.HandleFunc("/ws", serveWs)
}

func StartServer() {
	setupRoutes()
	http.ListenAndServe("0.0.0.0:8080", nil)
}
