let JSON/Type = ./Prelude/JSON/Type
let JSON/array = ./Prelude/JSON/array
let Map/keyValue = ./Prelude/Map/keyValue

let Option-Type = < Bool: Bool | JSON: JSON/Type >
let option = \(default: Option-Type) -> \(descr: Text) ->
	{
		type = merge {Bool = \(b: Bool) -> "bool", JSON = \(j: JSON/Type) -> "json"} default,
		default = default,
		descr = descr
	}
let default-bool = Option-Type.Bool True
let default-json = Option-Type.JSON (JSON/array ([] : List JSON/Type))
let option-command-disabling = option default-bool "If it's on, the command will work."
let key-option = Map/keyValue {type: Text, default: Option-Type, descr: Text}

in [
	key-option "cmd_8ball" option-command-disabling,
	key-option "ascii" option-command-disabling,
	key-option "autoresponse_file" (option default-json
		"This will be the file used when auto-responding to messages."),
	key-option "autoresponses" (option default-bool
		"If it's on, the bot will respond with preprogrammed messages when a keyword is said. Use `l.settings autoresponse_file` to see the preprogrammed messages."),
	key-option "bible" option-command-disabling,
	key-option "bitcoin" option-command-disabling,
	key-option "convert" option-command-disabling,
	key-option "dino" option-command-disabling,
	key-option "feedback" option-command-disabling,
	key-option "knockknock" option-command-disabling,
	key-option "minesweeper" option-command-disabling,
	key-option "ping" option-command-disabling,
	key-option "reddit" option-command-disabling,
	key-option "roll" option-command-disabling,
	key-option "say" option-command-disabling,
	key-option "server" option-command-disabling,
    key-option "useless" option-command-disabling,
	key-option "user_" option-command-disabling
]