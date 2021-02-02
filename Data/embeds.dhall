let embed = ./embed.dhall
let icons = ./icons.dhall

let icon-title = \(name: Text) -> \(icon-url: Text) ->
	Some embed.Author::{name = Some name, icon_url = Some icon-url}

in {
	`command disabled` = embed.Embed::{
		title = Some "Command Disabled!",
		description = Some "This command was disabled in the settings by an admin."
	},
	
	`command not found` = embed.Embed::{
		title = Some ":x: Command Not Found | Use `l.help` for command list"
	},
	
	`reddit error` = embed.Embed::{
		description = Some "Error, you did not provide a subreddit (starting with `r/`) or a user (starting with `u/`) You can use `l.help reddit` for help.",
		author = icon-title "Wrong Arguments" icons.reddit
	},
	
	`bitcoin error` = embed.Embed::{
		title = Some ":anger: Error, currency not found",
		description = Some "Current list of currencies: [Official Website](https://www.coindesk.com/price/bitcoin)"
	},

	`user error` = embed.Embed::{
		title = Some ":anger: Error",
		description = Some "No user detected. Tag someone by using @user."
	},
	
	`convert more args` = embed.Embed::{
		title = Some ":x: Error",
		description = Some "Type `l.help convert` for information on how to use the command."
	},
	
	`convert success` = embed.Embed::{
		title = Some ":white_check_mark: File Successfully Converted!"
	},
	
	`convert error converting` = embed.Embed::{
		title = Some ":x: Error while converting file → Link/Image not supported"
	},
	
	`convert error downloading` = embed.Embed::{
		title = Some ":x: Error while downloading → File too big or not supported"
	},
	
	`roll error` = embed.Embed::{
		description = Some "Your input is too big to calculate."
	},
	
	`roll more args` = embed.Embed::{
		description = Some "Roll using DnD rules. (Example: 2d6, where 2 is the number of dice to roll, and 6 is the number of sides on each die.)"
	},
	
	`settings more args` = embed.Embed::{
		description = Some "Not enough arguments were given to change an option, for help with `l.settings`, please use `l.help settings`.",
		author = icon-title "Not Enough Arguments" icons.settings
	},
	
	`settings not admin` = embed.Embed::{
		description = Some "You're not an admin, you can't access the settings.",
		author = icon-title "Denied Access" icons.settings
	},
	
	`bible no book` = embed.Embed::{
		description = Some "You need to pass a book from the Bible to search in.",
		author = icon-title "No Book Given" icons.bible
	},
	
	`bible wrong chapter order` = embed.Embed::{
		description = Some "The inputted chapter to end at comes before the chapter to start at.",
		author = icon-title "Reversed Chapter Order" icons.bible
	},
	
	`bible wrong verse order` = embed.Embed::{
		description = Some "The inputted verse to end at comes before the verse to start at.",
		author = icon-title "Reversed Verse Order" icons.bible
	},
	
	secret = embed.Embed::{
		description = Some "Send me a screenshot if you can get Ladbot to send this embed in Discord :)"
	}
}