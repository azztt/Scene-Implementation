import { Grid } from "@mui/material";
import React from "react";

const VerticalSpace = ({spacing}) => (
    <Grid container style={{height: `${spacing}px`}}/>
);

export default VerticalSpace