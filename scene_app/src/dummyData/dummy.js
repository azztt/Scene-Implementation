import * as utils from "../utils/utils"

export const dummy = {
    rooms: [
        {
            id: "1",
            name: "Room 1"
        },
        {
            id: "2",
            name: "Room 2"
        }
    ],
    devices: [
        {
            id: "1",
            name: "fan 1",
            roomId: "1",
            parameters: "speedLevels:4",
            status: "power:ON|speed:3",
            type: "FAN"
        },
        {
            id: "2",
            name: "color led 2",
            roomId: "1",
            parameters: "brightLevels:5",
            status: "power:ON|brightness:2|color:(250,50,70)",
            type: "CLIGHT"
        },
        {
            id: "3",
            name: "doorlock 3",
            roomId: "2",
            parameters: "",
            status: "power:ON|status:ON",
            type: "DLOCK"
        },
        {
            id: "4",
            name: "ac 4",
            roomId: "2",
            parameters: "tempRange:(16,30)",
            status: "power:ON|temperature:20|fanSpeed:MID|swingState:ON|mode:COOL",
            type: "AC"
        },
        {
            id: "5",
            name: "ac 4",
            roomId: "2",
            parameters: "tempRange:(16,30)",
            status: "power:ON|temperature:20|fanSpeed:MID|swingState:ON|mode:COOL",
            type: "AC"
        },
    ]
};

export const deviceObjects = dummy.devices.map((device) => {
    const statusObject = utils.readDeviceStatus(device);
    const paramObject = utils.readDeviceParams(device);
    return ({
        id: device.id,
        roomId: device.roomId,
        name: device.name,
        type: device.type,
        ...statusObject,
        ...paramObject
    });
})