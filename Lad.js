"use strict";

var discord = require("discord.js");
var auth = require("./auth.json");
var autoresponses = require("./autoresponses.json");

var client = new discord.Client();

client.on("ready", () => {
	console.log(`${client.user.tag} is logged in!`);
});

client.on("message", msg => {
	if(msg.author.username != "Lad") {
		var text = msg.content.toLowerCase().replace(/\s/, "");
		
		for(let pair of autoresponses) {
			for(let keyword of pair.keywords) {
				if(text.match(keyword)) {
					msg.channel.send(
						pair.responses[Math.floor(Math.random() * pair.responses.length)]
					);
					return;
				}
			}
		}
	}
});

client.login(auth.token);