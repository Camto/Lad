let Prelude = ./Prelude/package.dhall
let JSON = Prelude.JSON

let Option-Type = < Bool: Bool | JSON: JSON.Type >
let option = \(default: Option-Type) -> \(descr: Text) ->
	{
		type = merge {Bool = \(b: Bool) -> "bool", JSON = \(j: JSON.Type) -> "json"} default,
		default = default,
		descr = descr
	}
let default-bool = Option-Type.Bool True
let default-json = Option-Type.JSON (JSON.array ([] : List JSON.Type))
let option-command-disabling = option default-bool "If it's on, the command will work."

in

{
	autoresponses = option default-bool
		"If it's on, the bot will respond with preprogrammed messages when a keyword is said. Use `l.settings autoresponse_file` to see the preprogrammed messages.",
	
	autoresponse_file = option default-json
		"This will be the file used when auto-responding to messages.",
	
	bible = option default-bool
		"If it's on, the command will work. Use `l.help bible` for more information.",
	dino = option-command-disabling,
	ping = option-command-disabling,
	say = option-command-disabling,
	reddit = option-command-disabling,
	ascii = option-command-disabling,
	bitcoin = option-command-disabling
}