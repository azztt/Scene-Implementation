# Schema of SQL database

## Table `device`

`id`: string  
`type`: string eg: "AC", "FAN", etc  
`parameters`: string eg: "speedLevels:5|tempRange:(14,16)"  
`status`: string eg: "brightness:3|color:(250,134,150)"

## Table `scene`

`id`: string  
`roomId`: string  
`deviceIds`: string  
`deviceConfigs`: string eg: "device1 status string||device2 status string||..."

## Table `room`

`id`: string
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
