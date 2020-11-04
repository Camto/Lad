let List/map = ./Prelude/List/map
let Map/Entry = ./Prelude/Map/Entry
let Text/concatSep = ./Prelude/Text/concatSep
let JSON/Type = ./Prelude/JSON/Type

let Embed = ./Embed.dhall
let icons = ./icons.dhall
let options = ./options.dhall

let icon-title = \(name: Text) -> \(icon-url: Text) ->
	Some Embed.Author::{name = Some name, icon_url = Some icon-url}

in {
	`command disabled` = Embed.Embed::{
		title = Some "Command Disabled!",
		description = Some "This command was disabled in the settings by an admin."
	},
	
	`command not found` = Embed.Embed::{
		title = Some ":x: Command Not Found | Use `l.help` for command list"
	},
	
	`reddit error` = Embed.Embed::{
		description = Some "Error, you did not provide a subreddit (starting with `r/`) or a user (starting with `u/`) You can use `l.help reddit` for help.",
		author = icon-title "Wrong Arguments" icons.reddit
	},
	
	`bitcoin error` = Embed.Embed::{
		title = Some ":anger: Error, currency not found",
		description = Some "Current list of currencies: [Official Website](https://www.coindesk.com/price/bitcoin)"
	},
	
	`convert help` = Embed.Embed::{
		title = Some "How to use `l.convert` for links",
		description = Some "Supports: BMP, DCX, EPS, GIF, IM, JPEG, PCD, PCX, PDF, PNG, PPM, PSD, TIFF, XBM, XPM",
		image = Some Embed.Image::{
			url = Some "https://media.discordapp.net/attachments/711140380384559186/730876183025287290/croppimmage.png?width=549&height=279"
		}
	},
	
	`convert more args` = Embed.Embed::{
		title = Some ":x: Error",
		description = Some "Type `l.help convert` for information on how to use the command."
	},
	
	`convert success` = Embed.Embed::{
		title = Some ":white_check_mark: File Successfully Converted!"
	},
	
	`convert error converting` = Embed.Embed::{
		title = Some ":x: Error while converting file → Link/Image not supported"
	},
	
	`convert error downloading` = Embed.Embed::{
		title = Some ":x: Error while downloading → File too big or not supported"
	},
	
	`bible help` = Embed.Embed::{
		title = Some "To search type NUMBER first; followed by BOOK",
		author = icon-title "Bible Help" icons.bible,
		fields = Some (List/map Embed.Field.Type Embed.Field.Type
			(\(field: Embed.Field.Type) -> field // {inline = Some False})
			[
				Embed.Field::{name = "Matthew", value = "5:9 | 28:19 | 5:28 | 6:5 | 21:18-22 | 11:30 | 12:33 | 18:8 | 18:9"},
				Embed.Field::{name = "Leviticus", value = "19:19 | 19:27 | 9:10 | 15:19-20 | 25:44-46 | 21:17-23"},
				Embed.Field::{name = "Deuteronomy", value = "22:28-29 | 25:11-1 | 23:1 | 31:8 | 33:27 | 25:11-12"},
				Embed.Field::{name = "Psalms", value = "23:1-6 | 46:1-3 | 9:9-10 | 34:10b | 32:7-8"},
				Embed.Field::{name = "Exodus", value = "8:1-14 | 21:7-8 | 15:2 | 33:14 | 23:19"},
				Embed.Field::{name = "Kings", value = "6:28-29 | 2:23-25 | 23:20-25"},
				Embed.Field::{name = "John", value = "3:3 | 14:14 | 14:6 | 3:16"},
				Embed.Field::{name = "Chronicles", value = "21:14-15 | 16:11"},
				Embed.Field::{name = "Ephesians", value = "2:8 | 6:5 | 5:4"},
				Embed.Field::{name = "Proverbs", value = "18:10 | 15:4"},
				Embed.Field::{name = "Isaiah", value = "41:10 | 26:3-4"},
				Embed.Field::{name = "Timothy", value = "6:6-9 | 3:16"},
				Embed.Field::{name = "Luke", value = "16:18 | 3:11"},
				Embed.Field::{name = "Peter", value = "5:8 | 2:18"},
				Embed.Field::{name = "Numbers", value = "31:17-18"},
				Embed.Field::{name = "Reverend", value = "21:8"},
				Embed.Field::{name = "Nehemiah", value = "8:10"},
				Embed.Field::{name = "Ezekiel", value = "47:11"},
				Embed.Field::{name = "Hebrews", value = "12:1"},
				Embed.Field::{name = "Romans", value = "3:23"},
				Embed.Field::{name = "Genesis", value = "1:1"},
				Embed.Field::{name = "Samuel", value = "6:19"}
			])
	},
	
	`roll error` = Embed.Embed::{
		description = Some "Your input is too big to calculate."
	},
	
	`roll more args` = Embed.Embed::{
		description = Some "Roll using DnD rules. (Example: 2d6, where 2 is the number of dice to roll, and 6 is the number of sides on each die.)"
	},
	
	`settings help` = Embed.Embed::{
		description =
			let Option = Map/Entry Text {type: Text, default: < Bool: Bool | JSON: JSON/Type >, descr: Text}
			let option-list = Text/concatSep "\n\n" (List/map Option Text (\(option: Option) -> "`${option.mapKey}`: ${option.mapValue.descr}") options)
			in Some ''
			To change an option, use `l.settings <option name> <value>` <value> can be on or off.
			
			${option-list}'',
		author = icon-title "Settings Help" icons.settings
	},
	
	`settings more args` = Embed.Embed::{
		description = Some "Not enough arguments were given to change an option, for help with `l.settings`, please use `l.help settings`.",
		author = icon-title "Not Enough Arguments" icons.settings
	},
	
	`settings not admin` = Embed.Embed::{
		description = Some "You're not an admin, you can't access the settings.",
		author = icon-title "Denied Access" icons.settings
	}
}