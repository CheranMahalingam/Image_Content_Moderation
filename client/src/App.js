import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Amplify from "aws-amplify";
import { withAuthenticator } from "@aws-amplify/ui-react";
import ImagePage from "./pages/ImagePage";

Amplify.configure({
  Auth: {
    region: `${process.env.REACT_APP_REGION}`,
    userPoolId: `${process.env.REACT_APP_USER_POOL_ID}`,
    userPoolWebClientId: `${process.env.REACT_APP_USER_POOL_CLIENT_ID}`
  },
});

function App() {
  return (
    <>
      <Router>
        <Switch>
          <Route exact path="/" component={ImagePage} />
        </Switch>
      </Router>
    </>
  );
}

export default withAuthenticator(App);
