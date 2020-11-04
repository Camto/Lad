let command = \(cmd: Text) -> \(msg: Text) -> {cmd = cmd, msg = msg}

in [
	command "help"
		"Show this message.",
	command "ascii"
		"Returns your message in ASCII art!",
	command "bible"
		"Returns a random bible verse. For verses, do `l.help bible`.",
	command "bitcoin"
		"Get the current price of bitcoin with a wide range of currencies to choose from.",
	command "convert"
		"Converts a file type to another file type. Type `l.help convert` for all file types.",
	command "dino"
		"Use `l.dino` for a random dinosaur, `l.dino <dinosaur name here>` to find the dinosaur with that name.",
	command "ping"
		"Responds with pong.",
	command "reddit"
		"Sends a link to a random reddit post.",
	command "roll"
		"Roll using DnD rules. (Example: 2d6, where 2 is the number of dice to roll, and 6 is the number of sides on each die.)",
	command "say"
		"Make the bot say something.",
	command "settings"
		"Change Lad's options, like enabling or disabling certain commands. Can only be used by admins."
]