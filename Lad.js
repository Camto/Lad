"use strict";

var discord = require("discord.js");
var auth = require("./auth.json");

var client = new discord.Client();
var timeout_channel;

client.on("ready", () => {
	console.log(`${client.user.tag} is logged in!`);
	timeout_channel = client.channels.fetch("709639641568903179")
		.then(channel => {timeout_channel = channel;});
});

client.on("voiceStateUpdate", (old_st, new_st) => {
	console.log(new_st.channel.name);
});

client.login(auth.token);