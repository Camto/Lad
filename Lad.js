"use strict";

var discord = require("discord.js");
var auth = require("./auth.json");

var client = new discord.Client();

// Logging in the bot 
client.on("ready", () => {
	console.log(`${client.user.tag} is logged in!`);
});

client.login(auth.token);