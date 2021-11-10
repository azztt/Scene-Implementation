import React, { Fragment, useEffect, useState } from "react";
import { Paper, Grid, 
    Typography, Menu, 
    MenuItem, Button, Tooltip, Select } from "@mui/material";
import { withStyles } from "@mui/styles";
import AddButton from "../components/AddButton";
import NewRoomForm from "../components/NewRoomForm";
import NewDeviceForm from "../components/NewDeviceForm";
// import {dummy, deviceObjects} from "../dummyData/dummy";
import DeviceCard from "../components/DeviceCard";
import NewSceneForm from "../components/NewSceneForm";
import RoomCard from "../components/RoomCard";
import VerticalSpace from "../components/VerticalSpace";
import * as utils from "../utils/utils";

const styles = (theme) => ({
    container: {
        width: "100vw",
        height: "100vh",
        overflow: "hidden"
    },
    paper: {
        border: "3px solid black",
        height: "80%",
        width: "100%"
    },

});

const DashboardMin = (props) => {
    const { classes } = props;
    const [anchorEl, setAnchorEl] = useState(null);
    const addPopOpen = Boolean(anchorEl);
    const onAddClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const [dataState, setDataState] = useState({
        rooms: [],
        devices: [],
        configs: [],
        scenes: [],
    });

    // const [currentRoom, setCurrentRoom] = useState(dataState.rooms.length > 0 ? {
    //     room: dataState.rooms[0],
    //     idx: 0,
    // } : {
    //     room: {
    //         id: "0",
    //         name: "No room"
    //     },
    //     idx: 0,
    // });

    // const [currentScene, setCurrentScene] = useState(dataState.scenes.length > 0 ? {
    //     scene: dataState.scenes[0],
    //     idx: 0,
    // } : {
    //     scene: {
    //         id: "0",
    //         name: "No scene"
    //     },
    //     idx: 0,
    // });

    const [currentRoom, setCurrentRoom] = useState({
        room: {
            id: "0",
            name: "No room"
        },
        idx: 0,
    });

    const [currentScene, setCurrentScene] = useState({
        scene: {
            id: "0",
            name: "No scene"
        },
        idx: 0,
    });

    const [wsClient, setwsClient] = useState(new WebSocket("ws://localhost:8080/ws"));

    useEffect(() => {
        // const client = new WebSocket("ws://localhost:8080/ws");
        // console.log(JSON.stringify(dataState));
        wsClient.onopen = (e) => {
            console.log("connected to websocket");
            wsClient.send(JSON.stringify({
                req: "getEverything",
            }));
        };

        wsClient.onmessage = (messageEvent) => {
            const message = JSON.parse(messageEvent.data);
            console.log("message received: ", message);
            const res = message.res;

            if (message.message === "FAILED") {
                console.log("Error from server: " + message.error);
            } else if (res === "getEverything") {
                const data = message.data;
                console.log("message data: ", data);
                setDataState({
                    rooms: data.rooms ? data.rooms.map(room => utils.toNativeRoom(room)) : [],
                    devices: data.devices.map((deviceRes) => {
                        const device = utils.toNativeDevice(deviceRes)
                        // console.log("native devive object", device);
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
                    }),
                    scenes: data.scenes ? data.scenes.map(scene => utils.toNativeScene(scene)) : [],
                    configs: data.configs.map(conf => utils.toNativeConfig(conf)),
                });
                if (currentRoom.room.name === "No room") {
                    if (dataState.rooms.length > 0) {
                        setCurrentRoom({
                            room: dataState.rooms[0],
                            idx: 0,
                        });
                    }
                }
                if (currentScene.scene.name === "No scene") {
                    if (dataState.scenes.length > 0) {
                        setCurrentRoom({
                            scene: dataState.scenes[0],
                            idx: 0,
                        });
                    }
                }
            } else if (res === "createScene") {
                const data = message.data;
                console.log("message data: ", data);
                const newScene = data.scene;
                const newConfigs = data.configs;

                setDataState({
                    ...dataState,
                    scenes: [...dataState.scenes, newScene],
                    configs: [...dataState.configs, newConfigs],
                });
            } else if (res === "createRoom") {
                const data = message.data;
                console.log("message data: ", data);
                const newRoom = data.room;
                setDataState({
                    ...dataState,
                    rooms: [...dataState.rooms, newRoom],
                });
            } else if (res === "createDevice") {
                const data = message.data;
                console.log("message data: ", data);
                const newDevice = data.device;

                const deviceObject = [newDevice].map((device) => {
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
                })[0];

                setDataState({
                    ...dataState,
                    devices: [...dataState.devices, deviceObject],
                });
            } else if (res === "delDevice") {
                const data = message.data;
                console.log("message data: ", data);
                const devId = data.deviceId;

                setDataState({
                    ...dataState,
                    devices: dataState.devices.filter(dev => dev.id !== devId),
                });
            }
        }
        return () => {
            wsClient.close();
        }
        // setwsClient(client);
    }, []);

    const [formStates, setFormStates] = useState({
        newRoomForm: false,
        newDeviceForm: false,
        newSceneForm: false,
        roomDialog: false,
    });

    const toggleNewRoomForm = () => {
        setFormStates({
            ...formStates,
            newRoomForm: !formStates.newRoomForm,
        });
    };

    const toggleNewDeviceForm = () => {
        setFormStates({
            ...formStates,
            newDeviceForm: !formStates.newDeviceForm
        });
    };

    const toggleNewSceneForm = () => {
        setFormStates({
            ...formStates,
            newSceneForm: !formStates.newSceneForm,
        });
    };

    const toggleRoomDialog = () => {
        setFormStates({
            ...formStates,
            roomDialog: !formStates.roomDialog,
        });
    };

    const submitNewRoom = (roomData, cb) => {
        console.log("creating new room: ", roomData);
        const request = {
            req: "createRoom",
            body: {
                ...roomData
            },
        }
        wsClient.send(JSON.stringify(request));
        // wsClient.send(JSON.stringify({
        //     req: "getEverything",
        // }));
        cb();
    };

    const submitEditRoom = (roomData, cb) => {
        console.log(roomData);
        cb();
    };

    const submitNewDevice = (deviceData, cb) => {
        console.log("creating new device: ", deviceData);
        const devOb = deviceData;
        wsClient.send(JSON.stringify({
            req: "createDevice",
            body: {
                ...devOb,
            },
        }));
        // wsClient.send(JSON.stringify({
        //     req: "getEverything",
        // }));
        cb();
    };
    
    const submitNewScene = (sceneData, cb) => {
        console.log("creating new scene: ", sceneData);
        const newSceneName = sceneData.name;
        const devs = sceneData.devices;

        const devConfigs = devs.map(dev => utils.getDeviceConfig(dev));

        const reqBody = {
            name: newSceneName,
            deviceConfigs: devConfigs,
        };

        console.log("new scene body: ", reqBody);

        wsClient.send(JSON.stringify({
            req: "createScene",
            body: reqBody,
        }));
        wsClient.send(JSON.stringify({
            req: "getEverything",
        }));

        cb();
    };

    const setScene = (sceneId) => {
        console.log("setting scene: ", sceneId);
        wsClient.send(JSON.stringify({
            req: "setScene",
            body: {
                sceneId,
            },
        }));
    }

    const deleteDevice = (idx) => {
        console.log("deleting device: ", dataState.devices[idx]);
        wsClient.send(JSON.stringify({
            req: "delDevice",
            body: {
                deviceId: dataState.devices[idx].id,
            },
        }));
        wsClient.send(JSON.stringify({
            req: "getEverything",
        }));
    }

    return (
        <Grid container className={classes.container} justifyContent="center" alignItems="center">
            <Grid item xs={11}>
                <Typography variant="h2">
                    Scene Implementation
                </Typography>
            </Grid>
            <Grid item component={Paper} xs={11} className={classes.paper} container justifyContent="space-between" alignContent="flex-start">
                <Grid item xs={4} container justifyContent="flex-start">
                {/* add item button */}
                    <AddButton onClickHandler={onAddClick}/>
                    <Tooltip title="Add device to the current room" placement="top">
                        <Button variant="outlined" onClick={toggleNewDeviceForm}>
                            Add device
                        </Button>
                    </Tooltip>
                    <Menu
                        anchorEl={anchorEl}
                        open={addPopOpen}
                        onClose={() => setAnchorEl(null)}
                        anchorOrigin={{
                            vertical: "center",
                            horizontal: "right"
                        }}
                    >
                        <MenuItem onClick={toggleNewRoomForm}>Room</MenuItem>
                        <MenuItem onClick={toggleNewSceneForm}>Scene</MenuItem>
                    </Menu>
                    <NewRoomForm 
                        open={formStates.newRoomForm}
                        onCloseHandler={toggleNewRoomForm}
                        submit={(data, cb) => submitNewRoom(data, cb)}
                    />
                    {
                        dataState.rooms.length === 0 ?
                        null :
                        <NewDeviceForm 
                            open={formStates.newDeviceForm}
                            onCloseHandler={toggleNewDeviceForm}
                            submit={(data, cb) => submitNewDevice(data, cb)}
                            roomId={dataState.rooms[currentRoom.idx] ? dataState.rooms[currentRoom.idx].id : "0"}
                        />
                    }
                    <NewSceneForm
                        open={formStates.newSceneForm}
                        allDevices={dataState.devices}
                        allRooms={dataState.rooms}
                        onCloseHandler={toggleNewSceneForm}
                        submit={(data, cb) => submitNewScene(data, cb)}
                    />
                </Grid>
                <Grid item xs={4} container justifyContent="flex-end">
                {/* other buttons on right */}
                    
                </Grid>
                <Grid style={{height: "100%"}} item xs={6} style={{padding: "8px"}} container justifyContent="space-evenly" alignContent="center">
                    <Grid item xs={4}>
                        Current Room
                        <Select
                            labelId="currentRoomSelectorLabel"
                            id="currentRoomSelector"
                            defaultValue={0}
                            value={dataState.rooms.length > 0 ? currentRoom.idx : 0}
                            label="Current room"
                            onChange={(e) => setCurrentRoom({
                                room: dataState.rooms[e.target.value],
                                idx: e.target.value,
                            })}
                            fullWidth
                            margin="dense"
                        >
                            {
                                dataState.rooms.length > 0 ?
                                dataState.rooms.map((_, idx) => (
                                    <MenuItem key={idx} value={idx}>
                                        {dataState.rooms[idx].name}
                                    </MenuItem>
                                )) :
                                <MenuItem value={0}>No room</MenuItem>
                            }
                        </Select>
                    </Grid>
                    <Grid item xs={4}>
                        Current Scene
                        <Select
                            labelId="currentSceneSelectorLabel"
                            id="currentSceneSelector"
                            defaultValue={0}
                            value={dataState.scenes.length > 0 ? currentScene.idx : 0}
                            label="Current Scene"
                            onChange={(e) => {
                                setCurrentScene({
                                    scene: dataState.scenes[e.target.value],
                                    idx: e.target.value,
                                });
                                // setScene(dataState.scenes[e.target.value].id);
                            }}
                            fullWidth
                            margin="dense"
                        >
                            {
                                dataState.scenes.length > 0 ?
                                dataState.scenes.map((_, idx) => (
                                    <MenuItem value={idx} onClick={(e) => setScene(dataState.scenes[idx].id)}>
                                        {dataState.scenes[idx].name}
                                    </MenuItem>
                                )) :
                                <MenuItem value={0}>No scene</MenuItem>
                            }
                        </Select>
                    </Grid>
                    {/* {
                        dataState.rooms.length === 0 ?
                        <Typography variant="h4" textAlign="center" style={{color: "grey"}}>
                            No rooms added yet
                        </Typography> :
                        dataState.rooms.map((room, idx) => (
                            <Grid style={{cursor: "pointer"}} margin={2} item xs={4}>
                                <RoomCard
                                    key={idx}
                                    allDevices={dataState.devices}
                                    room={room}
                                    onSaveClick={(data, cb) => submitEditRoom(data, cb)}
                                    onClickHandler={toggleRoomDialog}
                                />
                            </Grid>
                        ))
                    } */}
                </Grid>
                <Grid item xs={6} style={{height: "65vh", overflow: "auto"}} container justifyContent="center" alignContent="flex-start">
                    {
                        dataState.rooms.length === 0?
                        <Typography variant="h4" textAlign="center" style={{color: "grey"}}>
                            No rooms added yet
                        </Typography> :
                        dataState.devices.filter(dev => dev.roomId === dataState.rooms[currentRoom.idx].id).length === 0 ?
                        <Typography variant="h4" textAlign="center" style={{color: "grey"}}>
                            No devices added in this room yet
                        </Typography> :
                        dataState.devices.filter(dev => dev.roomId === dataState.rooms[currentRoom.idx].id).map((dev, idx) => (
                            <Fragment key={idx}>
                                <VerticalSpace spacing={2}/>
                                <Grid item xs={11}>
                                    <DeviceCard
                                        allRooms={dataState.rooms}
                                        device={dev}
                                        inDevice
                                        inScene={false}
                                        onSaveClick={(eDev) => {}}
                                        onDelete={() => deleteDevice(idx)}
                                    />
                                </Grid>
                                <VerticalSpace spacing={2}/>
                            </Fragment>
                        ))
                    }
                </Grid>
            </Grid>
        </Grid>
    );
}

export default withStyles(styles)(DashboardMin)