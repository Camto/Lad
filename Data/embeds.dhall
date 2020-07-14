let icons = ./icons.dhall

let title = \(title: Text) -> {title = title}
let title_descr = \(title: Text) -> \(description: Text) ->
	{title = title, description = description}
let name_val_field = \(name: Text) -> \(val: Text) ->
	{name = name, value = val, inline = False}
let icon_title = \(name: Text) -> \(icon_url: Text) ->
	{name = name, icon_url = icon_url}
let img = \(url: Text) -> {url = url}

in {
	`command disabled` = title_descr
		"Command Disabled!"
		"This command was disabled in the settings by an admin.",
	
	`command not found` = title
		":x: Command Not Found | Use `l.help` for command list",
	
	`reddit error` = {
		description = "Error, you did not provide a subreddit (starting with `r/`) or a user (starting with `u/`) You can use `l.help reddit` for help.",
		author = icon_title "Wrong Arguments" icons.reddit
	},
	
	`bitcoin error` = title_descr
		":anger: Error, currency not found"
		"Current list of currencies: [Official Website](https://www.coindesk.com/price/bitcoin)",
	
	`convert help` = {
		title = "How to use `l.convert` for links",
		description = "Supports: BMP, DCX, EPS, GIF, IM, JPEG, PCD, PCX, PDF, PNG, PPM, PSD, TIFF, XBM, XPM",
		image = img "https://media.discordapp.net/attachments/711140380384559186/730876183025287290/croppimmage.png?width=549&height=279"
	},
	
	`convert more args` = title_descr
		":x: Error"
		"Type `l.help convert` for information on how to use the command.",
	
	`convert success` = title ":white_check_mark: File Successfully Converted!",
	
	`convert error converting` = title ":x: Error while converting file → Link/Image not supported",
	
	`convert error downloading` = title ":x: Error while downloading → File too big or not supported",
	
	`bible help` = {
		title = "To search type NUMBER first; followed by BOOK",
		author = icon_title "Bible Help" icons.bible,
		fields = [
			name_val_field "Matthew" "5:9 | 28:19 | 5:28 | 6:5 | 21:18-22 | 11:30 | 12:33 | 18:8 | 18:9",
			name_val_field "Leviticus" "19:19 | 19:27 | 9:10 | 15:19-20 | 25:44-46 | 21:17-23",
			name_val_field "Deuteronomy" "22:28-29 | 25:11-1 | 23:1 | 31:8 | 33:27 | 25:11-12",
			name_val_field "Psalms" "23:1-6 | 46:1-3 | 9:9-10 | 34:10b | 32:7-8",
			name_val_field "Exodus" "8:1-14 | 21:7-8 | 15:2 | 33:14 | 23:19",
			name_val_field "Kings" "6:28-29 | 2:23-25 | 23:20-25",
			name_val_field "John" "3:3 | 14:14 | 14:6 | 3:16",
			name_val_field "Chronicles" "21:14-15 | 16:11",
			name_val_field "Ephesians" "2:8 | 6:5 | 5:4",
			name_val_field "Proverbs" "18:10 | 15:4",
			name_val_field "Isaiah" "41:10 | 26:3-4",
			name_val_field "Timothy" "6:6-9 | 3:16",
			name_val_field "Luke" "16:18 | 3:11",
			name_val_field "Peter" "5:8 | 2:18",
			name_val_field "Numbers" "31:17-18",
			name_val_field "Reverend" "21:8",
			name_val_field "Nehemiah" "8:10",
			name_val_field "Ezekiel" "47:11",
			name_val_field "Hebrews" "12:1",
			name_val_field "Romans" "3:23",
			name_val_field "Genesis" "1:1",
			name_val_field "Samuel" "6:19"
		]
	},
	
	`roll error` = {
		description = "Your input is too big to calculate."
	},
	
	`roll more args` = {
		description = "Roll using DnD rules. (Example: 2d6, where 2 is the number of dice to roll, and 6 is the number of sides on each die.)"
	},
	
	`settings more args` = {
		description = "Not enough arguments were given to change an option, for help with `l.settings`, please use `l.help settings`.",
		author = icon_title "Not Enough Arguments" icons.settings
	},
	
	`settings not admin` = {
		description = "You're not an admin, you can't access the settings.",
		author = icon_title "Denied Access" icons.settings
	}
}