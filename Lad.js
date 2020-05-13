"use strict";

var discord = require("discord.js");
var auth = require("./auth.json");
var autoresponses = require("./autoresponses.json");

var client = new discord.Client();

var swears = autoresponses.swears;
var responses = autoresponses.responses;

client.on("ready", () => {
	console.log(`${client.user.tag} is logged in!`);
});

client.on("message", msg => {
	if(msg.author.username != "Lad") {
		var text = msg.content.toLowerCase();
		for(let swear of swears) {
			if(text.match(swear)) {
				msg.channel.send(
					responses[Math.floor(Math.random() * responses.length)]
				);
				return;
			}
		}
	}
});

client.login(auth.token);