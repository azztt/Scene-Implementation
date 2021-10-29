package main

import (
	"encoding/json"
	"fmt"
	// "log"
	// "net/http"
	// MODELS "github.com/azztt/Scene-Implementation/models"
	// "github.com/gorilla/websocket"
)

type nums struct {
	Num1 int
	Num2 int
}
type Country struct {

	// defining struct variables
	Name      string
	Capital   string
	Continent string
}

func (c *Country) Create(name string, capital string, continent string) {
	c.Name = name
	c.Capital = capital
	c.Continent = continent
}

// main function
func main() {

	// defining a struct instance
	var country1 Country
	// var count interface{}

	// data in JSON format which
	// is to be decoded
	// Data := []byte(`{
	// 	"capiTal": "New Delhi",
	//     "name": "India",
	//     "continent": "Asia",
	// 	"num": {1},
	// }`)

	var cn Country = Country{
		Name:      "India",
		Capital:   "New Delhi",
		Continent: "Asia",
	}

	data, _ := json.Marshal(cn)
	// decoding country1 struct
	// from json format
	err := json.Unmarshal(data, &country1)

	if err != nil {

		// if error is not nil
		// print error
		fmt.Println(err)
	}
	// count = country1

	// printing details of
	// decoded data
	fmt.Println("Struct is:", country1)

	fmt.Printf("%s's capital is %s and it is in %s.\n", country1.Name,
		country1.Capital, country1.Continent)

	var c Country
	c.Create("India", "New Delhi", "Asia")
	// fmt.Printf("%s's capital is %s and it is in %s.\n", c.Name,
	// 	c.Capital, c.Continent)

	s := "srfvwasfve)"
	fmt.Println(s[:len(s)-1])
}
