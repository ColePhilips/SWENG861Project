// src/App.js
//import logo from './logo.svg';
import './App.css';
import React from 'react';
//import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
//import { Amplify } from 'aws-amplify';
//import awsExports from './aws-exports';
import ToDo from './ToDo';
//import AuthComponent from './Auth';

//Amplify.configure(awsExports);

const App = () => {
  return (
    <div className="App">
      <ToDo />
    </div>
  );
};

export default App;
