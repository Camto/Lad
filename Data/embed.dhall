let embed = ./dhall-discord/embed.dhall

in  embed with Embed = (embed.Embed with default.color = Some ./embed-color.dhall)