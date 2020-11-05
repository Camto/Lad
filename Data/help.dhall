let List/map = ./Prelude/List/map
let Map/Entry = ./Prelude/Map/Entry
let Text/concatSep = ./Prelude/Text/concatSep
let JSON/Type = ./Prelude/JSON/Type

let embed = ./embed.dhall
let icons = ./icons.dhall
let options = ./options.dhall

let icon-title = \(name: Text) -> \(icon-url: Text) ->
	Some embed.Author::{name = Some name, icon_url = Some icon-url}

let command = \(cmd: Text) -> \(msg: Text) -> \(embed: embed.Embed.Type) -> {cmd = cmd, msg = msg, embed = embed}

let no-help-embed = embed.Embed::{
	title = Some "There's no help available for this command yet."
}

in [
	command "help"
		"Show this message."
		no-help-embed,
	
	command "ascii"
		"Returns your message in ASCII art!"
		no-help-embed,
	
	command "bible"
		"Returns a random bible verse. For verses, do `l.help bible`."
		embed.Embed::{
			title = Some "To search type NUMBER first; followed by BOOK",
			author = icon-title "Bible Help" icons.bible,
			fields = Some (List/map embed.Field.Type embed.Field.Type
				(\(field: embed.Field.Type) -> field with inline = Some True)
				[
					embed.Field::{name = "Matthew", value = "5:9 | 28:19 | 5:28 | 6:5 | 21:18-22 | 11:30 | 12:33 | 18:8 | 18:9"},
					embed.Field::{name = "Leviticus", value = "19:19 | 19:27 | 9:10 | 15:19-20 | 25:44-46 | 21:17-23"},
					embed.Field::{name = "Deuteronomy", value = "22:28-29 | 25:11-1 | 23:1 | 31:8 | 33:27 | 25:11-12"},
					embed.Field::{name = "Psalms", value = "23:1-6 | 46:1-3 | 9:9-10 | 34:10b | 32:7-8"},
					embed.Field::{name = "Exodus", value = "8:1-14 | 21:7-8 | 15:2 | 33:14 | 23:19"},
					embed.Field::{name = "Kings", value = "6:28-29 | 2:23-25 | 23:20-25"},
					embed.Field::{name = "John", value = "3:3 | 14:14 | 14:6 | 3:16"},
					embed.Field::{name = "Chronicles", value = "21:14-15 | 16:11"},
					embed.Field::{name = "Ephesians", value = "2:8 | 6:5 | 5:4"},
					embed.Field::{name = "Proverbs", value = "18:10 | 15:4"},
					embed.Field::{name = "Isaiah", value = "41:10 | 26:3-4"},
					embed.Field::{name = "Timothy", value = "6:6-9 | 3:16"},
					embed.Field::{name = "Luke", value = "16:18 | 3:11"},
					embed.Field::{name = "Peter", value = "5:8 | 2:18"},
					embed.Field::{name = "Numbers", value = "31:17-18"},
					embed.Field::{name = "Reverend", value = "21:8"},
					embed.Field::{name = "Nehemiah", value = "8:10"},
					embed.Field::{name = "Ezekiel", value = "47:11"},
					embed.Field::{name = "Hebrews", value = "12:1"},
					embed.Field::{name = "Romans", value = "3:23"},
					embed.Field::{name = "Genesis", value = "1:1"},
					embed.Field::{name = "Samuel", value = "6:19"}
				])
		},
	
	command "bitcoin"
		"Get the current price of bitcoin with a wide range of currencies to choose from."
		embed.Embed::{
			title = Some "Bitcoin -> Currency Conversion",
			description = Some "To change the currency output on [CoinDesk](https://www.coindesk.com/price/bitcoin) (ex. USD, EUR, GBP):"
		},
	
	command "convert"
		"Converts a file type to another file type. Type `l.help convert` for all file types."
		embed.Embed::{
			title = Some "How to use `l.convert` for links",
			description = Some "Supports: BMP, DCX, EPS, GIF, IM, JPEG, PCD, PCX, PDF, PNG, PPM, PSD, TIFF, XBM, XPM",
			image = Some embed.Image::{
				url = Some "https://media.discordapp.net/attachments/711140380384559186/730876183025287290/croppimmage.png?width=549&height=279"
			}
		},
	
	command "dino"
		"Use `l.dino` for a random dinosaur, `l.dino <dinosaur name here>` to find the dinosaur with that name."
		no-help-embed,
	
	command "ping"
		"Responds with pong."
		no-help-embed,
	
	command "reddit"
		"Sends a link to a random reddit post."
		embed.Embed::{
			description = Some "The Reddit command searches for posts either in a subreddit (starting with `r/`) or by a user (starting with `u/`.)",
			author = icon-title "Reddit Help" icons.reddit,
			fields = Some [
				embed.Field::{name = "Getting from subreddits", value = ''
					Putting the subreddit name will get random posts from there. For example: `l.reddit r/aww`
					
					You can sort by:
					- `hot`
					- `new`
					- `rising`
					- `top`, where you can also specify if you want top of: `hour`, `day`, `week`, `month`, `year`, or `all`.
					- `controversial`
					
					For example: `l.reddit r/aww rising` or `l.reddit r/aww top year`
					
					After sorting, a number can be added at the end to specify how many posts you want to fetch. For example: `l.reddit r/aww hot 5`''
				},
				embed.Field::{name = "Getting from users", value = ''
					With users, you can get their profile information or their posts. For example `l.reddit u/camto about` will get that user's information, and `l.reddit u/camto posts` will get their newest posts.
					
					If getting posts, sorting and specifying the number of posts can be done the same way as it's done for subreddits. For example, `l.reddit u/camto posts top all 5` will get that user's top 5 posts they ever made.''}
			]
		},
	
	command "roll"
		"Roll using DnD rules. (Example: 2d6, where 2 is the number of dice to roll, and 6 is the number of sides on each die.)"
		no-help-embed,
	
	command "say"
		"Make the bot say something."
		no-help-embed,
	
	command "settings"
		"Change Lad's options, like enabling or disabling certain commands. Can only be used by admins."
		embed.Embed::{
			description =
				let Option = Map/Entry Text {type: Text, default: < Bool: Bool | JSON: JSON/Type >, descr: Text}
				let option-list = Text/concatSep "\n\n" (
					List/map Option Text (\(option: Option) -> "`${option.mapKey}`: ${option.mapValue.descr}") options)
				in Some ''
					To change an option, use `l.settings <option name> <value>` <value> can be on or off.
					
					${option-list}'',
			author = icon-title "Settings Help" icons.settings
		}
]