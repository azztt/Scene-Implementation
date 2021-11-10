import { Button, Dialog, DialogContent, DialogTitle, FormControlLabel, Grid, Radio, RadioGroup, TextField, Typography } from "@mui/material";
import React, { Fragment, useEffect, useState } from "react";
import { withStyles } from "@mui/styles";
import VerticalSpace from "./VerticalSpace";
import * as deviceTypes from "../utils/deviceTypes";
import DeviceCard from "./DeviceCard";

const styles = (theme) => ({
    content: {
        overflow: "hidden"
    }
});

const NewSceneForm = ({open, onCloseHandler, allRooms, allDevices, submit, classes}) => {
    // const origFormState = {
    //     name: "",
    //     devices: allDevices,
    // }
    // const [formState, setFormState] = useState({
    //     ...origFormState
    // });
    const [formState, setFormState] = useState({
        name: "",
        devices: [],
    });

    useEffect(() => {
        setFormState({
            name: "",
            devices: [...allDevices],
        });
    }, [allDevices])

    console.log("new scene form form state", formState);

    const onSaveDeviceConfig = (dev, idx, cb) => {
        let oldDevices = [...formState.devices];
        console.log("old device:", oldDevices[idx]);
        oldDevices.splice(idx, 1, dev);
        // oldDevices[idx] = {
        //     ...oldDevices[idx],
        //     dev,
        // };

        console.log("old device:", oldDevices[idx]);

        console.log("edited device config", dev);

        setFormState({
            ...formState,
            devices: oldDevices,
        });

        cb();
    };

    const closeForm = () => {
        // setFormState({
        //     ...origFormState
        // });
        onCloseHandler();
    };

    const submitForm = () => {
        submit(formState, closeForm);
    };

    const onNameChange = (e) => {
        e.preventDefault();
        setFormState({
            ...formState,
            name: e.target.value,
        });
    };

    return (
        <Dialog open={open} onClose={onCloseHandler} maxWidth="md">
            <DialogTitle>
                <Typography variant="h4">
                    New Scene
                </Typography>
                <TextField
                    fullWidth
                    required
                    id="sceneName"
                    name="name"
                    variant="outlined"
                    color="secondary"
                    label="Name of new scene"
                    value={formState.name}
                    margin="dense"
                    size="large"
                    onChange={onNameChange}
                />
            </DialogTitle>
            <DialogContent className={classes.content}>
                <Grid container justifyContent="center" alignItems="center" style={{width: "100%"}}>
                    <Grid className={classes.content} item xs={11} container justifyContent="space-evenly" alignContent="center" alignItems="center">
                        <Grid item xs={12}>
                            <Typography textAlign="left" variant="h5">
                                Set device configurations:
                            </Typography>
                        </Grid>
                        <Grid
                            item xs={12}
                            container 
                            justifyContent="center"
                            alignItems="flex-start"
                            style={{
                                height: "100%",
                                overflow: "auto",
                            }} 
                        >
                            {
                                formState.devices.map((dev, idx) => (
                                    <Fragment key={idx}>
                                        <VerticalSpace spacing={6}/>
                                        <Grid item xs={11}>
                                            <DeviceCard
                                                allRooms={allRooms}
                                                device={dev}
                                                inDevice={false}
                                                inScene
                                                onSaveClick={(eDev, cb) => onSaveDeviceConfig(eDev, idx, cb)}
                                                onDelete={() => {}}
                                            />
                                            {/* <DeviceCard
                                                allRooms={dataState.rooms}
                                                device={dev}
                                                inDevice
                                                inScene={false}
                                                onSaveClick={(eDev) => {}}
                                                onDelete={() => deleteDevice(idx)}
                                            /> */}
                                        </Grid>
                                        <VerticalSpace spacing={6}/>
                                    </Fragment>
                                ))
                            }
                        </Grid>
                    </Grid>  
                    <VerticalSpace spacing={16}/>
                    <Grid item xs={11} container justifyContent='space-evenly' alignContent="center">
                        <Grid item xs={5} container justifyContent="center">
                            <Button variant="contained" fullWidth onClick={submitForm}>
                                Save Scene
                            </Button>
                        </Grid>
                        <Grid item xs={5} container justifyContent="center">
                            <Button variant="outlined" fullWidth onClick={closeForm}>
                                Cancel
                            </Button>
                        </Grid>
                    </Grid>
                </Grid>
            </DialogContent>
        </Dialog>
    );
}

export default withStyles(styles)(NewSceneForm);