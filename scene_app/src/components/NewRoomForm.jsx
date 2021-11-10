import { Button, Dialog, DialogContent, DialogTitle, Grid, TextField, Typography } from "@mui/material";
import React, { useState } from "react";
import { withStyles } from "@mui/styles";
import VerticalSpace from "./VerticalSpace";

const styles = (theme) => ({
    content: {
        overflow: "hidden"
    }
});

const NewRoomForm = ({open, onCloseHandler, submit, classes}) => {
    const origFormState = {
        name: "",
    };
    const [formState, setFormState] = useState({
        ...origFormState
    });

    const onChangeHandler = (e) => {
        e.preventDefault();
        setFormState({
            ...formState,
            [e.target.name]: e.target.value
        });
    };

    const closeForm = () => {
        setFormState({
            ...origFormState
        });
        onCloseHandler();
    };

    return (
        <Dialog open={open} onClose={onCloseHandler}>
            <DialogTitle>
                <Typography variant="h4">
                    New Room
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
                                id="roomName"
                                name="name"
                                variant="outlined"
                                color="secondary"
                                label="Name of new room"
                                value={formState.name}
                                margin="dense"
                                size="small"
                                onChange={onChangeHandler}
                            />
                        </Grid>
                    </Grid>
                    <VerticalSpace spacing={16}/>
                    <Grid item xs={11} container justifyContent='space-evenly' alignContent="center">
                        <Grid item xs={5} container justifyContent="center">
                            <Button variant="contained" fullWidth onClick={() => submit(formState, closeForm)}>
                                Create Room
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

export default withStyles(styles)(NewRoomForm)