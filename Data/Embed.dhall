let Type_ = < rich | image | video | gifv | article | link >

let Footer = {
	Type = {
		text: Text,
		icon_url: Optional Text,
		proxy_icon_url: Optional Text
	},
	default = {icon_url = None Text, proxy_icon_url = None Text}
}

let Image = {
	Type = {
		url: Optional Text,
		proxy_url: Optional Text,
		height: Optional Natural,
		width: Optional Natural
	},
	default = {
		url = None Text,
		proxy_url = None Text,
		height = None Natural,
		width = None Natural
	}
}

let Thumbnail = Image

let Video = {
	Type = {
		url: Optional Text,
		height: Optional Natural,
		width: Optional Natural
	},
	default = {
		url = None Text,
		height = None Natural,
		width = None Natural
	}
}

let Provider = {
	Type = {name: Optional Text, url: Optional Text},
	default = {name = None Text, url = None Text}
}

let Author = {
	Type = {
		name: Optional Text,
		url: Optional Text,
		icon_url: Optional Text,
		proxy_icon_url: Optional Text
	},
	default = {
		name = None Text,
		url = None Text,
		icon_url = None Text,
		proxy_icon_url = None Text
	}
}

let Field = {
	Type = {
		name: Text,
		value: Text,
		inline: Optional Bool
	},
	default = {inline = None Bool}
}

let Embed = {
	Type = {
		title: Optional Text,
		type: Optional Type_,
		description: Optional Text,
		url: Optional Text,
		timestamp: Optional Text,
		color: Optional Natural,
		footer: Optional Footer.Type,
		image: Optional Image.Type,
		thumbnail: Optional Thumbnail.Type,
		video: Optional Video.Type,
		provider: Optional Provider.Type,
		author: Optional Author.Type,
		fields: Optional (List Field.Type)
	},
	default = {
		title = None Text,
		type = None Type_,
		description = None Text,
		url = None Text,
		timestamp = None Text,
		color = None Natural,
		footer = None Footer.Type,
		image = None Image.Type,
		thumbnail = None Thumbnail.Type,
		video = None Video.Type,
		provider = None Provider.Type,
		author = None Author.Type,
		fields = None (List Field.Type)
	}
}

in {
	Type = Type_,
	Footer = Footer,
	Image = Image,
	Thumbnail = Thumbnail,
	Video = Video,
	Provider = Provider,
	Author = Author,
	Field = Field,
	Embed = Embed
}