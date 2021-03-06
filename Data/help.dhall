let List/map = ./Prelude/List/map
let Text/default = ./Prelude/Text/default
let Map/Entry = ./Prelude/Map/Entry
let Text/concatSep = ./Prelude/Text/concatSep
let JSON/Type = ./Prelude/JSON/Type

let embed = ./embed.dhall
let icons = ./icons.dhall
let emojis = ./emojis.dhall
let options = ./options.dhall

let icon-title = \(name: Text) -> \(icon-url: Text) ->
	Some embed.Author::{name = Some name, icon_url = Some icon-url}

let command = \(cmd: Text) -> \(msg: Text) -> \(embed: embed.Embed.Type) -> {cmd, msg, embed}

let no-help-embed = embed.Embed::{
	title = Some "There's no help available for this command yet."
}

in [
	command "help"
		"Show this message."
		no-help-embed,
	
	command "8ball"
		"Ask the Magic 8-Ball for help."
		no-help-embed,
	
	command "ascii"
		"Returns your message in ASCII art!"
		no-help-embed,
	
	command "bible"
		"Returns a random bible verse."
		embed.Embed::{
			author = icon-title "Bible Help" icons.bible,
			description = Some ''
				Search for any verse in the King James Bible.
				
				How to use the command:
				
				- `l.bible` fetches a random bible verse from any book.
				- `l.bible <book>` fetches a random verse from that book. The book name can be shortened, so `l.bible gen` does the same thing as `l.bible genesis`.
				- `l.bible <book> <chapter>` fetches that chapter from the book.
				- `l.bible <book> <chapter>-<chapter>` fetches the chapters in that range from the book. For example: `l.bible joel 1-3`
				- `l.bible <book> <chapter>:<verse>` fetches that specific verse from the book. For example: `l.bible gen 1:10`
				- `l.bible <book> <chapter>:<verse>-<verse>` fetches the verses in that range from the book. For example: `l.bible joel 1:5-10`
				
				If a response has the ${emojis.reload} reaction, that reaction can be clicked to fetch another verse.
				
				If a response has the ${emojis.`right pointer`} reaction, it has multiple pages that can be viewed using the ${emojis.`left pointer`} and ${emojis.`right pointer`} reactions.''
		},
	
	command "crypto"
		"Get the current price of (USD) whichever cryptocurrency you choose. For details, do `l.help crypto`. Inputs in symbol form (ex. ETH, BTC, DOGE)"
		embed.Embed::{
			author = icon-title "Crypto Help" icons.bitcoin,
			description = Some "This command uses [CoinMarketCap](https://coinmarketcap.com/) for all the data. For a list of all the currencies click [here](https://coinmarketcap.com/all/views/all/)."
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
		embed.Embed::{
			author = icon-title "Dino Help" (Text/default (List/head Text icons.dinos)),
			description = Some "Use `l.dino` for a random dinosaur, `l.dino <dinosaur name here>` to find the dinosaur with that name."
		},
	
	command "feedback"
		"Use `l.feedback <message>` to send the message as feedback to the devs :)"
		no-help-embed,
	
	command "knockknock"
		"Just try it, you'll see :)"
		no-help-embed,
	
	command "laugh"
		"Bad jokes? Lad's got your back"
		no-help-embed,

	command "minesweeper"
		"Makes a Minesweeper board."
		embed.Embed::{
			title = Some ":bomb: Minesweeper Help",
			description = Some "To use `l.minesweeper`, you can either pass nothing, or three positive numbers for width, height, and number of mines, for example `l.minesweeper 7 13 15` would give a 7x13 board with 15 mines."
		},
	
	command "ping"
		"Responds with pong."
		no-help-embed,
	
	command "reddit"
		"Lets you browse subreddits."
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
					
					If getting posts, sorting and specifying the number of posts can be done the same way as it's done for subreddits. For example, `l.reddit u/camto posts top all 5` will get that user's top 5 posts they ever made.''
				}
			]
		},
	
	command "roll"
		"Roll using DnD rules. (Example: 2d6, where 2 is the number of dice to roll, and 6 is the number of sides on each die.)"
		embed.Embed::{
			title = Some ":game_die: Roll Help",
			description = Some "Roll using DnD rules. (Example: 2d6, where 2 is the number of dice to roll, and 6 is the number of sides on each die.)"
		},
	
	command "say"
		"Make the bot say something."
		embed.Embed::{
			title = Some "Say Help",
			description = Some "Use `l.say <anything>` to make the bot say anything."
		},
	
	command "server"
		"Return the server's info."
		embed.Embed::{
			title = Some "Get Server Info",
			description = Some "Use `l.server` to get the server's information."
		},
	
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
		},
	
	command "useless"
		"Do nothing. Use `l.help useless` for more information."
		embed.Embed::{
			title = Some "Do nothing",
			description = Some ''
				Use `l.useless` to do absolutely nothing, exactly once.
				This command has the following subcommands:
				1.
				2.
				3.
				4.
				5.''
		},
	
	command "user"
		"Return a user's info."
		embed.Embed::{
			title = Some "Get User Info",
			description = Some "Use `l.user <@user>` to get the user's information."
		},
	
	command "weather"
		"Get the current weather status for a specific city."
		embed.Embed::{
			author = icon-title "Weather Help" icons.weather,
			description = Some "`l.weather <city>` will return the weather status for the biggest city in the world with that name."
		}
]