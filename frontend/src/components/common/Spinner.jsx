/* eslint-disable react/prop-types */
import { Box } from "@mui/material";
import React from "react";
import { TailSpin } from "react-loader-spinner";
function Spinner(props) {
  return (
    <>
    <h1>Spinner</h1>
      <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        width: "100%",
        height: "100%",
        m: "1rem",
        p: "1rem",
        zIndex: 99,
      }}
    >
      <TailSpin
        visible={props.visible}
        color="#002648"
        ariaLabel="tail-spin-loading"
        radius="1"
        wrapperStyle={{}}
        wrapperClass=""
      />
    </Box>
    </>
    
  );
}

export default Spinner;
