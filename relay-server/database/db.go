package database

import (
	"database/sql"
	"fmt"
	"os"

	"github.com/go-sql-driver/mysql"
	"github.com/joho/godotenv"
	"path/filepath"
)

//database handle

var db *sql.DB

func ConnectDB() error {
	envPath, _ := filepath.Abs("./.env")
	var envErr error = godotenv.Load(envPath)
	if envErr != nil {
		fmt.Println("Could not connect to db, aborting server start...")
		return envErr
	}

	var config mysql.Config = mysql.Config{
		User:                 os.Getenv("DBUSER"),
		Passwd:               os.Getenv("DBPASS"),
		Net:                  "tcp",
		Addr:                 os.Getenv("DBADDR"),
		DBName:               "cpsdb",
		AllowNativePasswords: true,
	}

	// open database handle
	var err error
	db, err = sql.Open("mysql", config.FormatDSN())
	if err != nil {
		fmt.Println("Could not open db, aborting server start...")
		return err
	}

	// checking connection
	pingError := db.Ping()
	if pingError != nil {
		fmt.Sprintln("Could not verify connection to db, aborting server start...")
		return pingError
	}
	fmt.Println("Connection to database verified")
	return nil
}

func DisconnectDB() error {
	fmt.Println("Disconnecting from database...")
	err := db.Close()
	if err != nil {
		fmt.Println("Could not disconnect from database. try again")
		return err
	}
	fmt.Println("Disconnected from database")
	return nil
}
