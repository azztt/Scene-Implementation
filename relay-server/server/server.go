package server

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

// func setupRoutes(statusChannel chan map[string]interface{}) {
// 	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
// 		fmt.Fprintf(w, "Simple Server")
// 	})
// 	// setting up the websocket endpoint
// 	http.HandleFunc("/ws", func(rw http.ResponseWriter, r *http.Request) {
// 		serveWs(rw, r, statusChannel)
// 	})
// }

func rootHandler(c echo.Context) error {
	return c.JSON(http.StatusOK, map[string]interface{}{
		"message": "useless route",
	})
}

func StartServer(statusChannel chan map[string]interface{}) {
	// setupRoutes(statusChannel)
	server := echo.New()
	server.GET("/", rootHandler)
	server.GET("/ws", func(c echo.Context) error {
		return serveWs(c, statusChannel)
	})
	server.Logger.Fatal(server.Start("0.0.0.0:8080"))
	// http.ListenAndServe("0.0.0.0:8080", nil)
}
