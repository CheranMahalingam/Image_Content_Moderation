const { Auth } = require("aws-amplify");

export const getJwtCognito = async () => {
  const jwtToken = Auth.currentSession()
    .then((data) => data.getIdToken().getJwtToken())
    .catch((err) => console.log(err));
  return jwtToken;
};
