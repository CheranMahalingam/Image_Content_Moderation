const { Auth } = require("aws-amplify");

/**
 * Uses browser session to get authenticated user's jwt token
 * @returns {String} jwt token to provide authorization for API Gateway requests
 */
export const getJwtCognito = async () => {
  const jwtToken = Auth.currentSession()
    .then((data) => data.getIdToken().getJwtToken())
    .catch((err) => console.log(err));
  return jwtToken;
};
