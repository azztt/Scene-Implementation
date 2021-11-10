import { Card,
    Paper, 
    Grid, CardContent, 
    TextField, Typography,
    Tooltip, IconButton,
} from "@mui/material";
import CloseRoundedIcon from '@mui/icons-material/CloseRounded';
import DoneRoundedIcon from '@mui/icons-material/DoneRounded';
import ModeEditRoundedIcon from '@mui/icons-material/ModeEditRounded';
import React, { useState } from "react";

const RoomCard = ({room, allDevices, onSaveClick, onClickHandler}) => {
    const [editMode, setEditMode] = useState(false);

    const [editState, setEditState] = useState(editMode? {
        ...room
    } : null);

    const openEditMode = () => {
        setEditMode(true);
        setEditState(
            {
                ...room
            }
        );
    };

    const closeEditMode = () => {
        setEditMode(false);
        setEditState(null);
    }

    const saveEdits = () => {
        onSaveClick(editState);
        closeEditMode();
    };

    const onEditChange = (e) => {
        e.preventDefault();
        setEditState({
            ...editState,
            [e.target.name]: e.target.value,
        });
    };

    return (
        <Card onClick={onClickHandler} component={({children}) => <Paper elevation={5}>{children}</Paper>} key={room.id} variant="outlined">
            <CardContent>
                <Grid container justifyContent="space-between" alignContent="center">
                    <Grid item xs={6}>
                        {
                            editMode?
                            <TextField
                                required
                                id="editRoomName"
                                name="name"
                                variant="outlined"
                                color="secondary"
                                label="Name of room"
                                value={editState.name}
                                margin="dense"
                                size="small"
                                onChange={onEditChange}
                            /> :
                            <Typography textAlign="left" variant="h4">
                                {room.name}
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
                        </Grid> : 
                        <Grid container justifyContent="flex-end" item xs={6}>
                            <Tooltip title="Edit">
                                <IconButton onClick={openEditMode} placement="top">
                                    <ModeEditRoundedIcon color="primary"/>
                                </IconButton>
                            </Tooltip>
                        </Grid>
                    }
                    <Grid item xs={12} container justifyContent="space-evenly">
                        {
                            allDevices.filter(dev => dev.roomId === room.id).map((dev) => (
                                <Grid item xs={4}>
                                    <div style={{
                                        border: "1px grey solid",
                                        borderRadius: "3px",
                                    }}>
                                        <Typography variant="h6" textAlign="center">
                                            {dev.name}
                                        </Typography>
                                    </div>
                                </Grid>
                            ))
                        }
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    );
};

export default RoomCard;