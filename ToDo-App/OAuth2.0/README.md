# OAuth

$ npm init -y

$ npm install dotenv --save

$ npm install express ejs body-parser 

$node app.js //To start the server up on http://localhost:3000/

$ npm i mongoose //make sure mongoose is installed

$ npm i passport express-session //To allow passport as our middleware for node.js

$ npm install passport-google-oauth20 //install oauth2.0 package for google

$ npm install mongoose-findorcreate //install findorcreate package since passport tries to use it but mongoose or mongoDB doesnt currently have

For implementation for other media other than google you will need to install the corresponding passport package
such as $ npm install passport-facebook. As well as add there correesponding strategy and authentication.

For more info on how to update the implementation for Either Facebook or Github go to https://wulfi.hashnode.dev/a-step-by-step-guide-to-oauth-20-implementing-sign-in-with-google-facebook-and-github

# Google Strategy
![alt text](image.png)<br/>
Use google secret to create secure setup for session ID cookies. 
The use of findorcrete to either find prior session of user or create new one.

# Google Authentication
![alt text](image-1.png)<br/>
The google scope profile will ask for the users information to allow passport to authenticate through OAuth2.0.
Then it will redirect to secrets to check authentication if fails/errors then will throw the user back to login screen with failureRedirect.
If succeeds then the user is thrown to route secrets.
Secrets would work as the main page the user is thrown to when they are authenticated so it would be the main page of you application.

# Serialization error handeling
![alt text](image-2.png)<br/>
Serialization to fix syncronization of users so that the site will not error.
