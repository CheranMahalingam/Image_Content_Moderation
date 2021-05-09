import { getJwtCognito } from "./apiUtils";

/**
 * Gets temporary credentials to upload an image directly to a s3 bucket
 * @param {Boolean} isPublic whether the image should be public or private
 * @returns {Object} API Gateway response containing the presigned url
 */
export const getPresignedUrlPut = async (isPublic) => {
  if (isPublic) {
    var eventUri = `${process.env.REACT_APP_SERVICE_URI}/upload/public`;
  } else {
    var eventUri = `${process.env.REACT_APP_SERVICE_URI}/upload/private`;
  }

  const response = await fetch(eventUri, {
    headers: {
      Authorization: `${await getJwtCognito()}`,
    },
  })
    .then((res) => res.json())
    .catch((err) => console.log(err));
  return response;
};

/**
 * Gets temporary credentials to get the images directly from a s3 bucket
 * @param {Boolean} isPublic whether the images are private or public
 * @returns {Object} API Gateway response containing an array of the presigned urls
 */
export const getPresignedUrlGet = async (isPublic) => {
  if (isPublic) {
    var eventUri = `${process.env.REACT_APP_SERVICE_URI}/view-image/public`;
  } else {
    var eventUri = `${process.env.REACT_APP_SERVICE_URI}/view-image/private`;
  }
  const response = await fetch(eventUri, {
    headers: {
      Authorization: `${await getJwtCognito()}`,
    },
  })
    .then((res) => res.json())
    .catch((err) => console.log(err));
  return response;
};

/**
 * Uploads an image to a s3 bucket
 * @param {Object} presignedResponse API Gateway response containing the presigned url
 * @param {File} file the image the user wants to upload
 * @returns API Gateway response indicating whether the upload was successful
 */
export const uploadImage = async (presignedResponse, file) => {
  let binary = atob(file.split(",")[1]);
  let array = [];
  for (let i = 0; i < binary.length; i++) {
    array.push(binary.charCodeAt(i));
  }
  let blobData = new Blob([new Uint8Array(array)], { type: "image/jpeg" });
  const s3Uri = presignedResponse.response;
  const response = await fetch(s3Uri, {
    headers: {
      "Content-Type": "image/jpeg",
    },
    method: "PUT",
    body: blobData,
  })
    .then((res) => console.log(res))
    .catch((err) => console.log(err));
  return response;
};

/**
 * Gets the image uri to view the image in the react app
 * @param {Object} presignedResponse API Gateway response containing an array of the presigned urls
 * @returns {Array} image URIs 
 */
export const viewImages = async (presignedResponse) => {
  const s3Uris = presignedResponse.response;
  let imageUri = [];
  if (s3Uris) {
    for (let uri of s3Uris) {
      const response = await fetch(uri).catch((err) => console.log(err));
      imageUri.push(response);
    }
  }
  return imageUri;
};
