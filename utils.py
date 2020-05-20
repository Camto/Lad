import json

lad_id = 709644595104972890
embed_color = 0xe07bb8
settings = {}

def get_json(filename):
	file = open(f"./Data/{filename}.json", encoding = "utf-8")
	data = json.load(file)
	file.close()
	return data

icons = get_json("icons")

def get_setting(guild_id, setting):
	return guild_id not in settings or settings[guild_id][setting]