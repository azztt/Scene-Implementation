import React, { useState } from "react";
import { Paper, Grid, Typography, Popover, Menu, MenuItem, Divider } from "@mui/material";
import { withStyles } from "@mui/styles";
import AddButton from "../components/AddButton";
import NewRoomForm from "../components/NewRoomForm";
import NewDeviceForm from "../components/NewDeviceForm";
import {dummy, deviceObjects} from "../dummyData/dummy";
import DeviceCard from "../components/DeviceCard";
import NewSceneForm from "../components/NewSceneForm";
import RoomCard from "../components/RoomCard";

const styles = (theme) => ({
    container: {
        width: "100vw",
        height: "100vh"
    },
    paper: {
        border: "3px solid black",
        height: "80%",
        width: "100%"
    },

});

const Dashboard = (props) => {
    const { classes } = props;
    const [anchorEl, setAnchorEl] = useState(null);
    const addPopOpen = Boolean(anchorEl);
    const onAddClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const [dataState, setDataState] = useState({
        rooms: dummy.rooms,
        devices: deviceObjects,
        configs: [],
        scenes: [],
    });

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
        console.log(roomData);
        cb();
    };

    const submitEditRoom = (roomData, cb) => {
        console.log(roomData);
        cb();
    };

    const submitNewDevice = (deviceData, cb) => {
        console.log(deviceData);
        cb();
    };
    
    const submitNewScene = (sceneData, cb) => {
        console.log(sceneData);
        cb();
    };

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
                    <NewDeviceForm 
                        open={formStates.newDeviceForm}
                        onCloseHandler={toggleNewDeviceForm}
                        submit={(data, cb) => submitNewDevice(data, cb)}
                        roomId="134134"
                    />
                    <NewSceneForm
                        open={formStates.newSceneForm}
                        allDevices={dataState.devices}
                        allRooms={dataState.rooms}
                        onCloseHandler={toggleNewSceneForm}
                        submit={(data, cb) => submitNewScene(data, cb)}
                    />
                </Grid>
                <Grid item xs={4}>
                    <Typography variant="h3" textAlign="center">
                        Rooms
                    </Typography>
                </Grid>
                <Grid item xs={4} container justifyContent="flex-end">
                {/* other buttons on right */}
                    <AddButton />
                </Grid>
                <Grid item xs={11} style={{padding: "8px"}} container alignContent="center">
                    {
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
                    }
                </Grid>
            </Grid>
        </Grid>
    );
}

export default withStyles(styles)(Dashboard)