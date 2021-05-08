import React from "react";
import Typography from "@material-ui/core/Typography";

function FileDetails(props) {
  const { file } = props;

  return (
    <>
      <Typography>
        {`File Name: ${file.name}`}
        <br />
        {`File Type: ${file.type}`}
        <br />
        {`File Size: ${file.size}`}
      </Typography>
    </>
  );
}

export default FileDetails;
