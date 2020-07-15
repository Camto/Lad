let List/map = ./Prelude/List/map
let icons = ./icons.dhall

let icon_title = \(name: Text) -> \(icon_url: Text) ->
	{name = name, icon_url = icon_url}

in {
	`command disabled` = {
		title = "Command Disabled!",
		description = "This command was disabled in the settings by an admin."
	},
	
	`command not found`.title = ":x: Command Not Found | Use `l.help` for command list",
	
	`reddit error` = {
		description = "Error, you did not provide a subreddit (starting with `r/`) or a user (starting with `u/`) You can use `l.help reddit` for help.",
		author = icon_title "Wrong Arguments" icons.reddit
	},
	
	`bitcoin error` = {
		title = ":anger: Error, currency not found",
		description = "Current list of currencies: [Official Website](https://www.coindesk.com/price/bitcoin)"
	},
	
	`convert help` = {
		title = "How to use `l.convert` for links",
		description = "Supports: BMP, DCX, EPS, GIF, IM, JPEG, PCD, PCX, PDF, PNG, PPM, PSD, TIFF, XBM, XPM",
		image.url = "https://media.discordapp.net/attachments/711140380384559186/730876183025287290/croppimmage.png?width=549&height=279"
	},
	
	`convert more args` = {
		title = ":x: Error",
		description = "Type `l.help convert` for information on how to use the command."
	},
	
	`convert success`.title = ":white_check_mark: File Successfully Converted!",
	
	`convert error converting`.title = ":x: Error while converting file → Link/Image not supported",
	
	`convert error downloading`.title = ":x: Error while downloading → File too big or not supported",
	
	`bible help` = {
		title = "To search type NUMBER first; followed by BOOK",
		author = icon_title "Bible Help" icons.bible,
		fields = List/map {name: Text, value: Text} {name: Text, value: Text, inline: Bool}
			(\(field: {name: Text, value: Text}) -> field // {inline = False})
			[
				{name = "Matthew", value = "5:9 | 28:19 | 5:28 | 6:5 | 21:18-22 | 11:30 | 12:33 | 18:8 | 18:9"},
				{name = "Leviticus", value = "19:19 | 19:27 | 9:10 | 15:19-20 | 25:44-46 | 21:17-23"},
				{name = "Deuteronomy", value = "22:28-29 | 25:11-1 | 23:1 | 31:8 | 33:27 | 25:11-12"},
				{name = "Psalms", value = "23:1-6 | 46:1-3 | 9:9-10 | 34:10b | 32:7-8"},
				{name = "Exodus", value = "8:1-14 | 21:7-8 | 15:2 | 33:14 | 23:19"},
				{name = "Kings", value = "6:28-29 | 2:23-25 | 23:20-25"},
				{name = "John", value = "3:3 | 14:14 | 14:6 | 3:16"},
				{name = "Chronicles", value = "21:14-15 | 16:11"},
				{name = "Ephesians", value = "2:8 | 6:5 | 5:4"},
				{name = "Proverbs", value = "18:10 | 15:4"},
				{name = "Isaiah", value = "41:10 | 26:3-4"},
				{name = "Timothy", value = "6:6-9 | 3:16"},
				{name = "Luke", value = "16:18 | 3:11"},
				{name = "Peter", value = "5:8 | 2:18"},
				{name = "Numbers", value = "31:17-18"},
				{name = "Reverend", value = "21:8"},
				{name = "Nehemiah", value = "8:10"},
				{name = "Ezekiel", value = "47:11"},
				{name = "Hebrews", value = "12:1"},
				{name = "Romans", value = "3:23"},
				{name = "Genesis", value = "1:1"},
				{name = "Samuel", value = "6:19"}
			]
	},
	
	`roll error`.description = "Your input is too big to calculate.",
	
	`roll more args`.description = "Roll using DnD rules. (Example: 2d6, where 2 is the number of dice to roll, and 6 is the number of sides on each die.)",
	
	`settings more args` = {
		description = "Not enough arguments were given to change an option, for help with `l.settings`, please use `l.help settings`.",
		author = icon_title "Not Enough Arguments" icons.settings
	},
	
	`settings not admin` = {
		description = "You're not an admin, you can't access the settings.",
		author = icon_title "Denied Access" icons.settings
	}
}