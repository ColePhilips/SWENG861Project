require('dotenv').config()
const express = require("express");
const bodyParser = require("body-parser");
const ejs = require("ejs");
const GoogleStrategy = require("passport-google-oauth20").Strategy; //require passport package for google
const findOrCreate = require('mongoose-findorcreate')
const session = require("express-session");
const passport = require("passport"); //Setup for passport to allow for cookies and sessions for the site
const app = express();
const mongoose = require("mongoose");

const userSchema = new mongoose.Schema ({ //New user schema for entry into the database, Will be updated with respected social media app
    email: String,
    username: String,
    googleId: String
});
userSchema.plugin(findOrCreate); //Plugin for database so it will either find pre existing user or create a new one
const User = new mongoose.model("User", userSchema);

app.use(express.static("public"));
app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({extended: true}));

// SET UP SESSION------below code comes from express-session
app.use(session({ 
  secret: process.env.PASSPORT_LONG_SECRET, 
  resave: false, 
  saveUninitialized: false
}));

//Database connection
mongoose.set("strictQuery", true);
main().catch(err => console.log(err));

async function main() {
    await mongoose.connect("mongodb+srv://ColePhilips:MongoDBDragon22!@monsterhunterdb.3kgwi.mongodb.net/testDB?retryWrites=true&w=majority&appName=MonsterHunterDB"); 
};

app.use(passport.initialize()); //initialize passport
app.use(passport.session()); //use of passport

// -------GOOGLE STRATEGY--------
passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: "http://34.227.109.255:3001/" //This will be changed to the web application URL so when the user is done authenticating this will be there endpoint, will also need to be updated on google site
  },
  //Callback function to find pre-existing info for user
  function(accessToken, refreshToken, profile, cb) {
    User.findOrCreate(
        { 
            googleId: profile.id
        }, 
        function (err, user) {
            return cb(err, user);
        }
    );
  }
));

//Fix errors when syncing users by serializing and deserializing them for callback
passport.serializeUser(function(user, cb) {
    process.nextTick(function() {
        return cb(null, user.id);
    });
});

passport.deserializeUser(function(user, cb) {
    process.nextTick(function() {
      return cb(null, user);
    });
});

app.get("/", function(req, res){
    res.render("home");
});

// -----GOOGLE AUTHENTICATION-----
app.get("/auth/google", 
    passport.authenticate("google", { scope: ["profile"] }) //setup anchors for redirecting to corresponding views
);
app.get("/auth/google/secrets", 
    passport.authenticate("google", { failureRedirect: "/login" }),
    function(req, res) {
      // Successful authentication, redirect home.
      res.redirect("/secrets");
});
  
app.get("/login", function(req, res){
    res.render("login");
});

app.get("/register", function(req, res){
    res.render("register");
});
app.get("/secrets", function(req, res){
    if (req.isAuthenticated()){
      res.render("secrets");
    } else {
      res.render("/login");
    }
});

//Adition of logout route
app.get("/logout", function(req, res){
    req.logout(function(err) {
        if (err) { 
            return next(err); 
        }
        res.redirect("/");
    });
});

app.listen(process.env.PORT, function(){
  console.log("Server started on port 3000.");
});



