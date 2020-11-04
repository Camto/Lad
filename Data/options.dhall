let Prelude = ./Prelude/package.dhall
let JSON = Prelude.JSON

let Option-Type = < Bool: Bool | JSON: JSON.Type >
let option = \(name: Text) -> \(default: Option-Type) -> \(descr: Text) ->
	{
		name = name,
		type = merge {Bool = \(b: Bool) -> "bool", JSON = \(j: JSON.Type) -> "json"} default,
		default = default,
		descr = descr
	}
let default-bool = Option-Type.Bool True
let default-json = Option-Type.JSON (JSON.array ([] : List JSON.Type))
let option-command-disabling = \(name: Text) -> option name default-bool "If it's on, the command will work."

in [
	option-command-disabling "ascii",
	option "autoresponse_file" default-json
		"This will be the file used when auto-responding to messages.",
	option "autoresponses" default-bool
		"If it's on, the bot will respond with preprogrammed messages when a keyword is said. Use `l.settings autoresponse_file` to see the preprogrammed messages.",
	option "bible" default-bool
		"If it's on, the command will work. Use `l.help bible` for more information.",
	option-command-disabling "bitcoin",
	option-command-disabling "dino",
	option-command-disabling "ping",
	option-command-disabling "reddit",
	option-command-disabling "say"
]