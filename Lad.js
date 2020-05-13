"use strict";

var discord = require("discord.js");
var auth = require("./auth.json");
var swears = require("./swears.json");

var client = new discord.Client();

client.on("ready", () => {
	console.log(`${client.user.tag} is logged in!`);
});

client.on("message", msg => {
	if(msg.author.username != "Lad") {
		msg.channel.send(swears[Math.floor(Math.random() * swears.length)]);
	}
});

client.login(auth.token);