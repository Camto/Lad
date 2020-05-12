"use strict";

var discord = require("discord.js");
var auth = require("./auth.json");

var client = new discord.Client();
var timeout_channel_id = "709639641568903179";
var timeout_channel;

client.on("ready", () => {
	console.log(`${client.user.tag} is logged in!`);
	timeout_channel = client.channels.fetch(timeout_channel_id)
		.then(channel => {timeout_channel = channel;});
});

client.on("voiceStateUpdate", (old_st, new_st) => {
	console.log(new_st.channel.name);
	if(timeout_channel && new_st.channel.id != timeout_channel_id) {
		new_st.setChannel(timeout_channel, "You are mega-muted.");
	}
});

client.login(auth.token);