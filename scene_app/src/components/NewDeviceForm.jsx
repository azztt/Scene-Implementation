import { Button, Dialog, DialogContent, DialogTitle, FormControlLabel, Grid, Radio, RadioGroup, TextField, Typography } from "@mui/material";
import React, { useState } from "react";
import { withStyles } from "@mui/styles";
import VerticalSpace from "./VerticalSpace";
import * as deviceTypes from "../utils/deviceTypes";
import { CloudDone } from "@mui/icons-material";

const styles = (theme) => ({
    content: {
        overflow: "hidden"
    }
});

const NewDeviceForm = ({open, onCloseHandler, roomId, submit, classes}) => {
    const origFormState = {
        roomId: roomId,
        name: "",
        type: "",
        minTemp: "16",
        maxTemp: "32",
        brightLevels: 4,
        speedLevels: 4,
    }
    const [formState, setFormState] = useState({
        ...origFormState
    });

    const onChangeHandler = (e) => {
        e.preventDefault();
        const name = e.target.name;
        if (name === "brightLevels" || name === "speedLevels") {
            if (parseInt(e.target.value) < 1) {
                return;
            }
        }
        if (name === "minTemp" || name === "maxTemp") {
            if (parseInt(e.target.value) === NaN) {
                console.log(true);
                return;
            }
        }
        setFormState({
            ...formState,
            [name]: e.target.value
        });
        console.log(formState);
        console.log(parseInt("23"));
    };

    const closeForm = () => {
        setFormState({
            ...origFormState
        });
        onCloseHandler();
    };

    const submitForm = () => {
        if (formState.type === "") {
            return
        }
        let data = {
            roomId: formState.roomId,
            name: formState.name,
            type: formState.type,
        };
        if (data.type === deviceTypes.AC_TYPE) {
            data = {
                ...data,
                tempRange: `(${formState.minTemp},${formState.maxTemp})`,
                // parameters: `tempRange:(${formState.minTemp},${formState.maxTemp})`,
                // status: `power:ON|temperature:${formState.minTemp}|fanSpeed:MID|swingState:ON|mode:COOL`,
            };
        } else if (data.type === deviceTypes.CLIGHT_TYPE) {
            data = {
                ...data,
                brightLevels: formState.brightLevels,
                // parameters: `brightLevels:${formState.brightLevels}`,
                // status: `power:ON|brightness:${formState.brightLevels}|color:(255,255,255)`,
            };
        } else if (data.type === deviceTypes.LIGHT_TYPE) {
            data = {
                ...data,
                brightLevels: formState.brightLevels,
                // parameters: `brightLevels:${formState.brightLevels}`,
                // status: `power:ON|brightness:${formState.brightLevels}`,
            };
        } else if (data.type === deviceTypes.FAN_TYPE) {
            data = {
                ...data,
                speedLevels: formState.speedLevels,
                // parameters: `speedLevels:${formState.speedLevels}`,
                // status: `power:ON|speed:${formState.speedLevels}`,
            };
        } else if (data.type === deviceTypes.DLOCK_TYPE) {
            data = {
                ...data,
                // parameters: "",
                // status: `power:ON|status:OFF`,
            };
        }
        submit(data, closeForm);
    };

    return (
        <Dialog open={open} onClose={onCloseHandler}>
            <DialogTitle>
                <Typography variant="h4">
                    New Device
                </Typography>
            </DialogTitle>
            <DialogContent className={classes.content}>
                <Grid container justifyContent="center" alignItems="center" style={{width: "100%"}}>
                <Grid item xs={11} container justifyContent="space-evenly" alignContent="center" alignItems="center">
                        <Grid item xs={2}>
                            <Typography textAlign="right" variant="h6">
                                Name:
                            </Typography>
                        </Grid>
                        <Grid item xs={8}>
                            <TextField
                                fullWidth
                                required
                                id="deviceName"
                                name="name"
                                variant="outlined"
                                color="secondary"
                                label="Name of new device"
                                value={formState.name}
                                margin="dense"
                                size="small"
                                onChange={onChangeHandler}
                            />
                        </Grid>
                        <VerticalSpace spacing={16}/>
                        <Grid item xs={11}>
                            <Typography textAlign="left" variant="h6">
                                Type of device:
                            </Typography>
                        </Grid>
                        <Grid item xs={12} container justifyContent="center">
                            <RadioGroup
                                aria-label="type"
                                name="type"
                                value={formState.type}
                                onChange={onChangeHandler}
                                row
                            >
                                <FormControlLabel
                                    value={deviceTypes.AC_TYPE} 
                                    control={<Radio />}
                                    label="AC"
                                    labelPlacement="end"
                                />
                                <FormControlLabel
                                    value={deviceTypes.CLIGHT_TYPE} 
                                    control={<Radio />}
                                    label="Color LED"
                                    labelPlacement="end"
                                />
                                <FormControlLabel
                                    value={deviceTypes.DLOCK_TYPE} 
                                    control={<Radio />}
                                    label="Door lock"
                                    labelPlacement="end"
                                />
                                <FormControlLabel
                                    value={deviceTypes.FAN_TYPE} 
                                    control={<Radio />}
                                    label="Fan"
                                    labelPlacement="end"
                                />
                                <FormControlLabel
                                    value={deviceTypes.LIGHT_TYPE} 
                                    control={<Radio />}
                                    label="Light"
                                    labelPlacement="end"
                                />
                            </RadioGroup>
                        </Grid>
                        <VerticalSpace spacing={16}/>
                        {
                            // AC form
                            formState.type === deviceTypes.AC_TYPE ?
                            <>
                                <Grid item xs={11}>
                                    <Typography textAlign="left" variant="h6">
                                        Temperature range (deg C):
                                    </Typography>
                                </Grid>
                                <Grid item xs={4}>
                                    <TextField
                                        fullWidth
                                        required
                                        id="minTemp"
                                        name="minTemp"
                                        variant="outlined"
                                        color="secondary"
                                        label="Min temp"
                                        value={formState.minTemp}
                                        // defaultValue={0}
                                        error={formState.maxTemp < formState.minTemp}
                                        margin="dense"
                                        size="small"
                                        onChange={onChangeHandler}
                                        type="number"
                                    />
                                </Grid>
                                <Grid item xs={4}>
                                    <TextField
                                        fullWidth
                                        required
                                        id="maxTemp"
                                        name="maxTemp"
                                        variant="outlined"
                                        color="secondary"
                                        label="Max temp"
                                        value={formState.maxTemp}
                                        // defaultValue={0}
                                        error={formState.maxTemp < formState.minTemp}
                                        margin="dense"
                                        size="small"
                                        onChange={onChangeHandler}
                                        type="number"
                                    />
                                </Grid>
                            </> : null
                        }
                        {
                            // AC form
                            formState.type === deviceTypes.CLIGHT_TYPE ||
                            formState.type === deviceTypes.LIGHT_TYPE ?
                            <>
                                <Grid item xs={4}>
                                    <Typography textAlign="left" variant="h6">
                                        Brightness levels:
                                    </Typography>
                                </Grid>
                                <Grid item xs={8}>
                                    <TextField
                                        fullWidth
                                        required
                                        id="brightLevele"
                                        name="brightLevels"
                                        variant="outlined"
                                        color="secondary"
                                        label="Levels"
                                        value={formState.brightLevels}
                                        // defaultValue={0}
                                        error={formState.brightLevels < 1}
                                        margin="dense"
                                        size="small"
                                        onChange={onChangeHandler}
                                        type="number"
                                    />
                                </Grid>
                            </> : null
                        }
                        {
                            // AC form
                            formState.type === deviceTypes.FAN_TYPE ?
                            <>
                                <Grid item xs={4}>
                                    <Typography textAlign="left" variant="h6">
                                        Speed levels:
                                    </Typography>
                                </Grid>
                                <Grid item xs={8}>
                                    <TextField
                                        fullWidth
                                        required
                                        id="speedLevels"
                                        name="speedLevels"
                                        variant="outlined"
                                        color="secondary"
                                        label="Levels"
                                        value={formState.speedLevels}
                                        // defaultValue={0}
                                        error={formState.speedLevels < 1}
                                        margin="dense"
                                        size="small"
                                        onChange={onChangeHandler}
                                        type="number"
                                    />
                                </Grid>
                            </> : null
                        }
                    </Grid>
                    <VerticalSpace spacing={16}/>
                    <Grid item xs={11} container justifyContent='space-evenly' alignContent="center">
                        <Grid item xs={5} container justifyContent="center">
                            <Button variant="contained" fullWidth onClick={submitForm}>
                                Create Device
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

export default withStyles(styles)(NewDeviceForm)