// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { Amplify } from 'aws-amplify';
import awsExports from './aws-exports';
import ToDo from './ToDo';
import AuthComponent from './Auth';

Amplify.configure(awsExports);

const App = () => {
  return (
    <Router>
      <Switch>
        <Route path="/todo" component={ToDo} />
        <Route path="/" component={AuthComponent} />
      </Switch>
    </Router>
  );
};

export default App;
