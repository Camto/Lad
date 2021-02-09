let List/map = ./Prelude/List/map
let List/concat = ./Prelude/List/concat

let embed = ./embed.dhall

let map_prefix = \(pre: Text) -> List/map Text Text (\(s: Text) -> pre ++ s)

let yes_responses = map_prefix ":smiley: " [
	"It is certain.",
	"It is decidedly so.",
	"Without a doubt.",
	"Yes – definitely.",
	"You may rely on it.",
	"As I see it, yes.",
	"Most likely.",
	"Outlook good.",
	"Yes.",
	"Signs point to yes."
]

let unsure_responses = map_prefix ":woozy_face: " [
	"Reply hazy, try again.",
	"Ask again later.",
	"Better not tell you now.",
	"Cannot predict now.",
	"Concentrate and ask again."
]

let no_responses = map_prefix ":no_entry_sign: " [
	"Don't count on it.",
	"My reply is no.",
	"My sources say no.",
	"Outlook not so good.",
	"Very doubtful."
]

let responses = List/concat Text [yes_responses, unsure_responses, no_responses]

in List/map Text embed.Embed.Type (\(response: Text) -> embed.Embed::{
	description = Some response
}) responses