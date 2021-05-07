import { getJwtCognito } from "./apiUtils";

export const getPresignedUrlPut = async (isPublic) => {
  if (isPublic) {
    var eventUri = `${process.env.REACT_APP_SERVICE_URI}/upload/public`;
  } else {
    var eventUri = `${process.env.REACT_APP_SERVICE_URI}/upload/private`;
  }

  const response = await fetch(eventUri, {
    headers: {
      Authorization: `${await getJwtCognito()}`,
    }
  })
    .then((res) => res.json())
    .catch((err) => console.log(err));
  return response;
};

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

export const viewImages = async (presignedResponse) => {
  console.log(presignedResponse);
  const s3Uris = presignedResponse.response;
  let imageUri = [];
  for (let uri of s3Uris) {
    const response = await fetch(uri).catch((err) => console.log(err));
    imageUri.push(response);
  }
  console.log(imageUri);
  return imageUri;
};
