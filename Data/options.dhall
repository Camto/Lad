let Prelude = ./Prelude/package.dhall
let JSON = Prelude.JSON
let Map/keyValue = ./Prelude/Map/keyValue

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
let keyOption = Map/keyValue {type: Text, default: Option-Type, descr: Text}

in [
	keyOption "ascii" option-command-disabling,
	keyOption "autoresponse_file" (option default-json
		"This will be the file used when auto-responding to messages."),
	keyOption "autoresponses" (option default-bool
		"If it's on, the bot will respond with preprogrammed messages when a keyword is said. Use `l.settings autoresponse_file` to see the preprogrammed messages."),
	keyOption "bible" option-command-disabling,
	keyOption "bitcoin" option-command-disabling,
	keyOption "dino" option-command-disabling,
	keyOption "ping" option-command-disabling,
	keyOption "reddit" option-command-disabling,
	keyOption "say" option-command-disabling
]