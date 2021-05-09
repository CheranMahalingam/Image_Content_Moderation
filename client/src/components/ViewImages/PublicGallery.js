import React, { useState, useEffect, useCallback } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Backdrop from "@material-ui/core/Backdrop";
import CircularProgress from "@material-ui/core/CircularProgress";
import { getPresignedUrlGet, viewImages } from "../../utils/imageUtils";

const useStyles = makeStyles((theme) => ({
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: "#fff",
  },
}));

function PublicGallery() {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);

  const classes = useStyles();

  const fetchImages = useCallback(async () => {
    const responseObj = await getPresignedUrlGet(true).catch((err) =>
      console.log(err)
    );
    if (responseObj) {
      setImages(await viewImages(responseObj));
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchImages();
  }, [fetchImages]);

  return (
    <>
      {images.length > 0 &&
        images.map((image, index) => {
          return (
            <>
              <img key={index} src={image.url} />
              <br />
            </>
          );
        })}
      <Backdrop className={classes.backdrop} open={loading}>
        <CircularProgress color="inherit" />
      </Backdrop>
    </>
  );
}

export default PublicGallery;
