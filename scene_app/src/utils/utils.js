import * as deviceTypes from "./deviceTypes";
import * as Str from "@supercharge/strings";

export const readAcStatus = (statusString) => {
    const params = statusString.split("|")
    const statusObject = {
        power: "",
        temperature: 0,
        fanSpeed: "",
        swingState: "",
        mode: "",
    }

    statusObject.power = params[0].split(":")[1]
    statusObject.temperature = parseInt(params[1].split(":")[1])
    statusObject.fanSpeed = params[2].split(":")[1]
    statusObject.swingState = params[3].split(":")[1]
    statusObject.mode = params[4].split(":")[1]

    return statusObject
}

export const readAcParams = (paramString) => {
    const params = paramString.split("|");
    const paramObject = {
        tempRange: params[0].split(":")[1],
    };
    return paramObject;
};

export const readCLightStatus = (statusString) => {
    const params = statusString.split("|")
    const statusObject = {
        power: "",
        brightness: 0,
        color: [0, 0, 0],
    }

    statusObject.power = params[0].split(":")[1]
    statusObject.brightness = parseInt(params[1].split(":")[1])
    let colors = params[2].split(":")[1]
    colors = colors.substr(1, colors.length - 2)
    statusObject.color = colors.split(",").map(val => parseInt(val))

    return statusObject
}

export const readLightParams = (paramString) => {
    const params = paramString.split("|");
    const paramObject = {
        brightLevels: params[0].split(":")[1],
    };
    return paramObject;
};

export const readDLockStatus = (statusString) => {
    const params = statusString.split("|")
    const statusObject = {
        power: params[0].split(":")[1],
        status: params[1].split(":")[1]
    }
    return statusObject
}

export const readDLockParams = (paramString) => {
    const params = paramString.split("|");
    const paramObject = {};
    return paramObject;
};

export const readFanStatus = (statusString) => {
    const params = statusString.split("|")
    console.log(params);
    const statusObject = {
        power: params[0].split(":")[1],
        speed : parseInt(params[1].split(":")[1])
    }
    console.log(statusObject);
    return statusObject
}

export const readFanParams = (paramString) => {
    const params = paramString.split("|");
    const paramObject = {
        speedLevels: params[0].split(":")[1],
    };
    return paramObject;
};

export const readLightStatus = (statusString) => {
    const params = statusString.split("|")
    const statusObject = {
        power: params[0].split(":")[1],
        brightness: parseInt(params[1].split(":")[1])
    }
    return statusObject
}

export const readDeviceParams = (device) => {
    switch (device.type) {
        case deviceTypes.AC_TYPE:
            return readAcParams(device.parameters);
        case deviceTypes.CLIGHT_TYPE:
            return readLightParams(device.parameters);
        case deviceTypes.LIGHT_TYPE:
            return readLightParams(device.parameters);
        case deviceTypes.DLOCK_TYPE:
            return readDLockParams(device.parameters);
        case deviceTypes.FAN_TYPE:
            return readFanParams(device.parameters);
    };
};

export const readDeviceStatus = (device) => {
    // console.log(device);
    switch (device.type) {
        case deviceTypes.AC_TYPE:
            return readAcStatus(device.status);
        case deviceTypes.CLIGHT_TYPE:
            return readCLightStatus(device.status);
        case deviceTypes.DLOCK_TYPE:
            return readDLockStatus(device.status);
        case deviceTypes.FAN_TYPE:
            return readFanStatus(device.status);
        case deviceTypes.LIGHT_TYPE:
            return readLightStatus(device.status);
    };
};

export const getDeviceObject = (device) => {
    if (device.type === "AC") {
        const devOb = {
            name: device.name,
            roomId: device.roomId,
            type: device.type,
            parameters: `tempRange:(${device.minTemp},${device.maxTemp})`,
            status: `power:ON|temperature:${device.minTemp}|fanSpeed:MID|swingState:ON|mode:COOL`,
        };
        return devOb;
    } else if (device.type === "CLIGHT") {
        const devOb = {
            name: device.name,
            roomId: device.roomId,
            type: device.type,
            parameters: `brightLevels:${device.brightLevels}`,
            status: `power:ON|brightness:${device.brightLevels}|color:(255,255,255)`,
        };
        return devOb;
    } else if (device.type === "DLOCK") {
        const devOb = {
            name: device.name,
            roomId: device.roomId,
            type: device.type,
            parameters: "",
            status: `power:ON|status:OFF`,
        };
        return devOb;
    } else if (device.type === "FAN") {
        const devOb = {
            name: device.name,
            roomId: device.roomId,
            type: device.type,
            parameters: `speedLevels:${device.speedLevels}`,
            status: `power:ON|speed:${device.speedLevels}`,
        };
        return devOb;
    } else if (device.type === "LIGHT") {
        const devOb = {
            name: device.name,
            roomId: device.roomId,
            type: device.type,
            parameters: `brightLevels:${device.brightLevels}`,
            status: `power:ON|brightness:${device.brightLevels}`,
        };
        return devOb;
    }
}

export const getDeviceConfig = (device) => {
    if (device.type === "AC") {
        const devOb = {
            deviceId: device.id,
            config: `power:${device.power}|temperature:${device.temperature}|fanSpeed:${device.fanSpeed}|swingState:${device.swingState}|mode:${device.mode}`,
        };
        return devOb;
    } else if (device.type === "CLIGHT") {
        const devOb = {
            deviceId: device.id,
            config: `power:${device.power}|brightness:${device.brightness}|color:(${device.color[0]},${device.color[1]},${device.color[2]})`,
        };
        return devOb;
    } else if (device.type === "DLOCK") {
        const devOb = {
            deviceId: device.id,
            config: `power:${device.power}|status:${device.status}`,
        };
        return devOb;
    } else if (device.type === "FAN") {
        const devOb = {
            deviceId: device.id,
            config: `power:${device.power}|speed:${device.speed}`,
        };
        return devOb;
    } else if (device.type === "LIGHT") {
        const devOb = {
            deviceId: device.id,
            config: `power:${device.power}|brightness:${device.brightness}`,
        };
        return devOb;
    }
}

export const parsetempRange = (tempRange) => {
    tempRange = tempRange.substr(1, tempRange.length - 2);
    const minMax = tempRange.split(",").map(val => parseInt(val));
    return minMax;
}

export const toNativeDevice = (dev) => {
    return {    
        id: dev.ID,
        name: dev.Name,
        roomId: dev.RoomId,
        parameters: dev.Parameters,
        status: dev.Status,
        type: dev.Type,
    };
};

export const toNativeRoom = (room) => {
    return {    
        id: room.ID,
        name: room.Name,
    };
};

export const toNativeScene = (scene) => {
    return {    
        id: scene.ID,
        name: scene.Name,
    };
};

export const toNativeConfig = (conf) => {
    return {    
        id: conf.ID,
        deviceId: conf.DeviceId,
        sceneId: conf.SceneId,
        deviceConfig: conf.DeviceConfig
    };
};
