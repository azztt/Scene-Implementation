import React from "react";
import { IconButton, Tooltip } from "@mui/material";
import AddCircleIcon from '@mui/icons-material/AddCircle';

const AddButton = ({onClickHandler}) => {
    return (
        <Tooltip placement="top" title="Add new items">
            <IconButton style={{padding: "8px"}} color="primary" size="large" onClick={onClickHandler}>
                <AddCircleIcon style={{width: "60px", height: "auto"}} fontSize="large"/>
            </IconButton>
        </Tooltip>
    )
}

export default AddButton;