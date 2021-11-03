# Schema of SQL database

## Table `device`

`id`: string  
`name`: string  
`parameters`: string eg: "speedLevels:5|tempRange:(14,16)"  
`status`: string eg: "brightness:3|color:(250,134,150)"  
`type`: string eg: "AC", "FAN", etc

## Table `scene`

`id`: string  
`name`: string  
`roomId`: string  
`deviceIds`: string  
`deviceConfigs`: string eg: "device1 status string||device2 status string||..."

## Table `room`

`id`: string  
`name`: string  
`deviceIds`: string eg: "id1,id2,..."

## New device request format in json

```json
{
    "room_id": string,
    "type": string,
    "name": string,
    ...other parameters for the concerned device
}
```
