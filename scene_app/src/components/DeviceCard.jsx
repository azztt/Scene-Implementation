import { Card, CardContent, 
    Grid, IconButton, Tooltip, 
    Typography, RadioGroup, 
    FormControlLabel, Radio, 
    Slider, TextField, Paper } from "@mui/material";
import React, { useEffect, useState } from "react";
import CloseRoundedIcon from '@mui/icons-material/CloseRounded';
import DoneRoundedIcon from '@mui/icons-material/DoneRounded';
import ModeEditRoundedIcon from '@mui/icons-material/ModeEditRounded';
import DeleteOutlineRoundedIcon from '@mui/icons-material/DeleteOutlineRounded';
import * as deviceTypes from "../utils/deviceTypes";
import {parsetempRange} from "../utils/utils";

const DeviceCard = ({device, allRooms, inDevice, inScene, onSaveClick, onDelete }) => {
    const [editMode, setEditMode] = useState(false);

    const [editState, setEditState] = useState(editMode? {
        ...device
    } : null);

    useEffect(() => {
        setEditState({
            ...device
        });
    }, [device]);

    const openEditMode = () => {
        setEditMode(true);
        setEditState(
            {
                ...device
            }
        );
    };

    const closeEditMode = () => {
        setEditMode(false);
        setEditState(null);
    }

    const saveEdits = () => {
        onSaveClick(editState, closeEditMode);
    };

    const onEditChange = (e) => {
        // e.preventDefault();
        setEditState({
            ...editState,
            [e.target.name]: e.target.value,
        });
    };

    const onRedChange = (e) => {
        setEditState({
            ...editState,
            color: [e.target.value, editState.color[1], editState.color[2]],
        });
    };

    const onGreenChange = (e) => {
        setEditState({
            ...editState,
            color: [editState.color[0], e.target.value, editState.color[2]],
        });
    };

    const onBlueChange = (e) => {
        setEditState({
            ...editState,
            color: [editState.color[0], editState.color[1], e.target.value],
        });
    };


    return (
        <Card component={({children}) => <Paper elevation={5}>{children}</Paper>} key={device.id} variant="outlined">
            <CardContent>
                <Grid container justifyContent="space-between" alignContent="center">
                    <Grid item xs={6}>
                        {
                            editMode && inDevice?
                            <TextField
                                required
                                id="editDeviceName"
                                name="name"
                                variant="outlined"
                                color="secondary"
                                label="Name of device"
                                value={editState.name}
                                margin="dense"
                                size="large"
                                onChange={onEditChange}
                            /> :
                            <Typography textAlign="left" variant="h4">
                                {device.name}
                            </Typography>
                        }
                    </Grid>
                    {
                        editMode?
                        <Grid container justifyContent="flex-end" item xs={6}>
                            <Tooltip title="Cancel edit" placement="top">
                                <IconButton onClick={closeEditMode}>
                                    <CloseRoundedIcon color="primary"/>
                                </IconButton>
                            </Tooltip>
                            <Tooltip title="Save edit">
                                <IconButton onClick={saveEdits} placement="top">
                                    <DoneRoundedIcon color="primary"/>
                                </IconButton>
                            </Tooltip>
                            {
                                inDevice?
                                <Tooltip title="Remove device">
                                    <IconButton onClick={onDelete? onDelete : () => {}} placement="top">
                                        <DeleteOutlineRoundedIcon color="error"/>
                                    </IconButton>
                                </Tooltip> : null
                            }
                        </Grid> : 
                        <Grid container justifyContent="flex-end" item xs={6}>
                            <Tooltip title="Edit">
                                <IconButton onClick={openEditMode} placement="top">
                                    <ModeEditRoundedIcon color="primary"/>
                                </IconButton>
                            </Tooltip>
                        </Grid>
                    }
                </Grid>
                <Grid item xs={4}>
                    <Typography variant="h6">
                        Power:
                    </Typography>
                </Grid>
                <Grid item xs={7}>
                    {
                        editMode && inScene ?
                        <RadioGroup
                            aria-label="power"
                            name="power"
                            value={editState.power}
                            onChange={onEditChange}
                            row
                        >
                            <FormControlLabel
                                value="ON" 
                                control={<Radio />}
                                label="ON"
                                labelPlacement="end"
                            />
                            <FormControlLabel
                                value="OFF" 
                                control={<Radio />}
                                label="OFF"
                                labelPlacement="end"
                            />
                        </RadioGroup> :
                        <Typography variant="h6">
                            {`${device.power}`}
                        </Typography>
                    }
                </Grid>
                {
                    device.type === deviceTypes.AC_TYPE ?
                    <>
                        <Grid container style={{width: "100%"}} justifyContent="flex-start" alignContent="center">
                            <Grid item xs={11}>
                                <Typography variant="h6">
                                    {`I am an Air Conditioner in room ${allRooms.filter((room) => room.id === device.roomId)[0].name}`}
                                </Typography>
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="h6">
                                    Temperature range:
                                </Typography>
                            </Grid>
                            <Grid item xs={7}>
                                <Typography variant="h6">
                                    {`${device.tempRange}`}
                                </Typography>
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="h6">
                                    Current temperature:
                                </Typography>
                            </Grid>
                            <Grid item xs={7}>
                                {
                                    editMode && inScene?
                                    <Slider
                                        value={editState.temperature} 
                                        step={1}
                                        name="temperature"
                                        color="secondary"
                                        valueLabelDisplay="auto"
                                        onChange={onEditChange}
                                        marks={Array.from({length: parsetempRange(editState.tempRange)[1]-parsetempRange(editState.tempRange)[0]+1}, (_,k)=> ({value: k+parsetempRange(editState.tempRange)[0]}))}
                                        min={parsetempRange(editState.tempRange)[0]}
                                        max={parsetempRange(editState.tempRange)[1]}
                                    />:
                                    <Typography variant="h6">
                                        {`${device.temperature}`}
                                    </Typography>
                                }
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="h6">
                                    Swing:
                                </Typography>
                            </Grid>
                            <Grid item xs={7}>
                                {
                                    editMode && inScene ?
                                    <RadioGroup
                                        aria-label="swingState"
                                        name="swingState"
                                        value={editState.swingState}
                                        onChange={onEditChange}
                                        row
                                    >
                                        <FormControlLabel
                                            value="ON" 
                                            control={<Radio />}
                                            label="ON"
                                            labelPlacement="end"
                                        />
                                        <FormControlLabel
                                            value="OFF" 
                                            control={<Radio />}
                                            label="OFF"
                                            labelPlacement="end"
                                        />
                                    </RadioGroup> :
                                    <Typography variant="h6">
                                        {`${device.swingState}`}
                                    </Typography>
                                }
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="h6">
                                    Fan speed:
                                </Typography>
                            </Grid>
                            <Grid item xs={7}>
                                {
                                    editMode && inScene ?
                                    <RadioGroup
                                        aria-label="fanSpeed"
                                        name="fanSpeed"
                                        value={editState.fanSpeed}
                                        onChange={onEditChange}
                                        row
                                    >
                                        <FormControlLabel
                                            value="LOW" 
                                            control={<Radio />}
                                            label="LOW"
                                            labelPlacement="end"
                                        />
                                        <FormControlLabel
                                            value="MID" 
                                            control={<Radio />}
                                            label="MID"
                                            labelPlacement="end"
                                        />
                                        <FormControlLabel
                                            value="HIGH" 
                                            control={<Radio />}
                                            label="HIGH"
                                            labelPlacement="end"
                                        />
                                    </RadioGroup> :
                                    <Typography variant="h6">
                                        {`${device.fanSpeed}`}
                                    </Typography>
                                }
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="h6">
                                    Mode:
                                </Typography>
                            </Grid>
                            <Grid item xs={7}>
                                {
                                    editMode && inScene ?
                                    <RadioGroup
                                        aria-label="mode"
                                        name="mode"
                                        value={editState.mode}
                                        onChange={onEditChange}
                                        row
                                    >
                                        <FormControlLabel
                                            value="COOL" 
                                            control={<Radio />}
                                            label="COOL"
                                            labelPlacement="end"
                                        />
                                        <FormControlLabel
                                            value="DRY" 
                                            control={<Radio />}
                                            label="DRY"
                                            labelPlacement="end"
                                        />
                                        <FormControlLabel
                                            value="FAN" 
                                            control={<Radio />}
                                            label="FAN"
                                            labelPlacement="end"
                                        />
                                    </RadioGroup> :
                                    <Typography variant="h6">
                                        {`${device.mode}`}
                                    </Typography>
                                }
                            </Grid>
                        </Grid>
                    </> : null
                }
                {
                    device.type === deviceTypes.CLIGHT_TYPE ?
                    <>
                        <Grid container style={{width: "100%"}} justifyContent="flex-start" alignContent="center">
                            <Grid item xs={11}>
                                <Typography variant="h6">
                                    {`I am a Color LED in room ${allRooms.filter((room) => room.id === device.roomId)[0].name}`}
                                </Typography>
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="h6">
                                    Brightness levels:
                                </Typography>
                            </Grid>
                            <Grid item xs={7}>
                                <Typography variant="h6">
                                    {`${device.brightLevels}`}
                                </Typography>
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="h6">
                                    Current brightness:
                                </Typography>
                            </Grid>
                            <Grid item xs={7}>
                                {
                                    editMode && inScene?
                                    <Slider
                                        value={editState.brightness} 
                                        step={1}
                                        name="brightness"
                                        color="secondary"
                                        valueLabelDisplay="auto"
                                        onChange={onEditChange}
                                        marks={Array.from({length: editState.brightLevels}, (_,k)=> ({value: k+1}))}
                                        min={1}
                                        max={editState.brightLevels}
                                    />:
                                    <Typography variant="h6">
                                        {`${device.brightness}`}
                                    </Typography>
                                }
                            </Grid>
                            <Grid item xs={4} container alignContent="center">
                                <Typography variant="h6">
                                    Current Color:
                                </Typography>
                            </Grid>
                            <Grid item xs={7} container alignContent="center">
                                {
                                    editMode && inScene?
                                    <Grid container justifyContent="space-between" alignContent="center">
                                        <Grid item xs={7} container justifyContent="center" alignContent="center">
                                            <Grid item xs={12}>
                                                R<Slider
                                                        value={editState.color[0]} 
                                                        step={1}
                                                        name="red"
                                                        color="secondary"
                                                        valueLabelDisplay="auto"
                                                        onChange={onRedChange}
                                                        marks={Array.from({length: 256}, (_,k)=> ({value: k}))}
                                                        min={0}
                                                        max={255}
                                                />
                                            </Grid>
                                            <Grid item xs={12}>
                                                G<Slider
                                                        value={editState.color[1]} 
                                                        step={1}
                                                        name="green"
                                                        color="secondary"
                                                        valueLabelDisplay="auto"
                                                        onChange={onGreenChange}
                                                        marks={Array.from({length: 256}, (_,k)=> ({value: k}))}
                                                        min={0}
                                                        max={255}
                                                />
                                            </Grid>
                                            <Grid item xs={12}>
                                                B<Slider
                                                        value={editState.color[2]} 
                                                        step={1}
                                                        name="blue"
                                                        color="secondary"
                                                        valueLabelDisplay="auto"
                                                        onChange={onBlueChange}
                                                        marks={Array.from({length: 256}, (_,k)=> ({value: k}))}
                                                        min={0}
                                                        max={255}
                                                />
                                            </Grid>
                                        </Grid>
                                        <Grid
                                            item xs={4}
                                            style={{
                                                width: "100%",
                                                height: "100%",
                                                backgroundColor: `rgb(${editState.color[0]},${editState.color[1]},${editState.color[2]})`
                                            }}
                                        />
                                    </Grid> :
                                    <Grid 
                                        container
                                        style={{
                                            height: "16px",
                                            width: "16px",
                                            backgroundColor: `rgb(${device.color[0]},${device.color[1]},${device.color[2]})`
                                        }}
                                    />
                                }
                            </Grid>
                        </Grid>
                    </> : null
                }
                {
                    device.type === deviceTypes.LIGHT_TYPE ?
                    <>
                        <Grid container style={{width: "100%"}} justifyContent="flex-start" alignContent="center">
                            <Grid item xs={11}>
                                <Typography variant="h6">
                                    {`I am a Light in room ${allRooms.filter((room) => room.id === device.roomId)[0].name}`}
                                </Typography>
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="h6">
                                    Brightness levels:
                                </Typography>
                            </Grid>
                            <Grid item xs={7}>
                                <Typography variant="h6">
                                    {`${device.brightLevels}`}
                                </Typography>
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="h6">
                                    Current brightness:
                                </Typography>
                            </Grid>
                            <Grid item xs={7}>
                                {
                                    editMode && inScene?
                                    <Slider
                                        value={editState.brightness} 
                                        step={1}
                                        name="brightness"
                                        color="secondary"
                                        valueLabelDisplay="auto"
                                        onChange={onEditChange}
                                        marks={Array.from({length: editState.brightLevels}, (_,k)=> ({value: k+1}))}
                                        min={1}
                                        max={editState.brightLevels}
                                    />:
                                    <Typography variant="h6">
                                        {`${device.brightness}`}
                                    </Typography>
                                }
                            </Grid>
                        </Grid>
                    </> : null
                }
                {
                    device.type === deviceTypes.DLOCK_TYPE ?
                    <>
                        <Grid container style={{width: "100%"}} justifyContent="flex-start" alignContent="center">
                            <Grid item xs={11}>
                                <Typography variant="h6">
                                    {`I am a Door Lock in room ${allRooms.filter((room) => room.id === device.roomId)[0].name}`}
                                </Typography>
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="h6">
                                    Lock State:
                                </Typography>
                            </Grid>
                            <Grid item xs={7}>
                                {
                                    editMode && inScene ?
                                    <RadioGroup
                                        aria-label="status"
                                        name="status"
                                        value={editState.status}
                                        onChange={onEditChange}
                                        row
                                    >
                                        <FormControlLabel
                                            value="ON" 
                                            control={<Radio />}
                                            label="ON"
                                            labelPlacement="end"
                                        />
                                        <FormControlLabel
                                            value="OFF" 
                                            control={<Radio />}
                                            label="OFF"
                                            labelPlacement="end"
                                        />
                                    </RadioGroup> :
                                    <Typography variant="h6">
                                        {`${device.status}`}
                                    </Typography>
                                }
                            </Grid>
                        </Grid>
                    </> : null
                }
                {
                    device.type === deviceTypes.FAN_TYPE ?
                    <>
                        <Grid container style={{width: "100%"}} justifyContent="flex-start" alignContent="center">
                            <Grid item xs={11}>
                                <Typography variant="h6">
                                    {`I am a Fan in room ${allRooms.filter((room) => room.id === device.roomId)[0].name}`}
                                </Typography>
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="h6">
                                    Speed levels:
                                </Typography>
                            </Grid>
                            <Grid item xs={7}>
                                <Typography variant="h6">
                                    {`${device.speedLevels}`}
                                </Typography>
                            </Grid>
                            <Grid item xs={4}>
                                <Typography variant="h6">
                                    Current speed:
                                </Typography>
                            </Grid>
                            <Grid item xs={7}>
                                {
                                    editMode && inScene?
                                    <Slider
                                        value={editState.speed} 
                                        step={1}
                                        name="speed"
                                        color="secondary"
                                        valueLabelDisplay="auto"
                                        onChange={onEditChange}
                                        marks={Array.from({length: editState.speedLevels}, (_,k)=> ({value: k+1}))}
                                        min={1}
                                        max={editState.speedLevels}
                                    />:
                                    <Typography variant="h6">
                                        {`${device.speed}`}
                                    </Typography>
                                }
                            </Grid>
                        </Grid>
                    </> : null
                }
            </CardContent>
        </Card>
    )
}

export default DeviceCard