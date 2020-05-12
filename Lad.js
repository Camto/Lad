"use strict";

var discord = require("discord.js");
var auth = require("./auth.json");

var client = new discord.Client();

client.on("ready", () => {
	console.log(`${client.user.tag} is logged in!`);
});

client.on("voiceStateUpdate", (old_st, new_st) => {
	console.log(new_st.channel.name);
});

client.login(auth.token);