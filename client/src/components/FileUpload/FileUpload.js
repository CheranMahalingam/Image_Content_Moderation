import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import Backdrop from "@material-ui/core/Backdrop";
import CircularProgress from "@material-ui/core/CircularProgress";
import FileDetails from "./FileDetails";
import { getPresignedUrlPut, uploadImage } from "../../utils/imageUtils";

const useStyles = makeStyles((theme) => ({
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: "#fff",
  },
}));

function FileUpload() {
  const [file, setFile] = useState("");
  const [image, setImage] = useState("");
  const [isFileSelected, setIsFileSelected] = useState(false);
  const [loading, setLoading] = useState(false);

  const classes = useStyles();

  const handleNewFile = (event) => {
    setFile(event.target.files[0]);
    setIsFileSelected(true);
    createImage(event.target.files[0]);
  };

  const handleUploadImage = async (isPublic) => {
    setLoading(true);
    const responseObj = await getPresignedUrlPut(isPublic).catch((err) =>
      console.log(err)
    );
    console.log(responseObj);
    await uploadImage(responseObj, image).catch((err) => console.log(err));
    setLoading(false);
  };

  const createImage = (file) => {
    let reader = new FileReader();
    reader.onload = (event) => {
      setImage(event.target.result);
    };
    reader.readAsDataURL(file);
  };

  return (
    <>
      <input type="file" accept="image/jpeg" onChange={handleNewFile} />
      <br />
      {isFileSelected ? <img src={URL.createObjectURL(file)} /> : null}
      <br />
      {isFileSelected ? <FileDetails file={file} /> : null}
      <br />
      <Button
        variant="contained"
        color="primary"
        onClick={() => handleUploadImage(false)}
      >
        Upload Image to Private Repository
      </Button>
      <Button
        variant="contained"
        color="primary"
        onClick={() => handleUploadImage(true)}
        style={{ marginLeft: 20 }}
      >
        Upload Image to Public Gallery
      </Button>
      <Backdrop className={classes.backdrop} open={loading}>
        <CircularProgress color="inherit" />
      </Backdrop>
    </>
  );
}

export default FileUpload;
