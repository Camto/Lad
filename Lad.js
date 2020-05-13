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
		var text = msg.content.toLowerCase();
		for(let swear of swears) {
			if(text.match(swear)) {
				msg.channel.send("WOAH WOAH WOAH THERE NO SWEARING IN THIS LAND");
				return
			}
		}
	}
});

client.login(auth.token);