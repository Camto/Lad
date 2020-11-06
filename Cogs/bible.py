import discord
from discord.ext import commands
import utils

import math
import itertools
import re
import random

from fuzzywuzzy import fuzz, process

bible = utils.get_yaml("bible")
book_names = list(map(lambda book: book["name"], bible))

search_chars = re.compile("[^A-Za-z0-9:\-;]")
book_name_parse = re.compile("\d?[A-Za-z]+")

# Starting the bible study.
class Bible(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def bible(self, ctx, *, args = None):
		if utils.get_setting(ctx.guild.id, "bible"):
			if args == None:
				await utils.menus.reload(self.client, ctx, random_passage_menu())
			else:
				try:
					args = search_chars.sub("", args)
					book_name_match = book_name_parse.match(args)
					if book_name_match:
						book_name = book_name_match.group(0)
						args = args[book_name_match.end():]
					else: raise(Exception("Moron: No book"))
					
					book_name = process.extractOne(book_name, book_names)[0]
					book = list(filter(lambda book: book["name"] == book_name, bible))[0]
					
					if args == "":
						await utils.menus.reload(self.client, ctx, random_passage_menu(book_name = book_name))
					else:
						passage_chunks = args.split(";")
						passages = list(itertools.chain(*map(
							lambda chunk: get_passage_chunk(book["chapters"], parse_passage_chunk(book["chapters"], chunk)),
							passage_chunks)))
						await utils.menus.list(self.client, ctx, chapter_menu(book_name, passages))
				except Exception as e:
					import traceback
					print(traceback.format_exc())
		else:
			await ctx.send(embed = utils.command_disabled)

def random_passage_menu(book_name = None):
	async def gen(_):
		while True:
			if book_name == None: book = random.choice(bible)
			else: book = list(filter(lambda book: book["name"] == book_name, bible))[0]
			chapters = book['chapters']
			chapter = random.randrange(len(chapters))
			verse = random.randrange(len(chapters[chapter]))
			yield passage_to_embed(chapters[chapter][verse], f"{book['name']} {chapter+1}:{verse+1}")
	return gen

def passage_to_embed(passage, loc):
	return (discord.Embed(
		description = passage,
		color = utils.embed_color)
		.set_author(
			name = loc,
			icon_url = utils.icons["bible"]))

def parse_passage_chunk(chapters, str_):
	if "-" in str_:
		start, end = str_.split("-")
		if ":" not in start:
			start_chapter = try_nat(start)
			start_verse = 1
			if ":" not in end:
				end_chapter = try_nat(end)
				if end_chapter > len(chapters): raise(Exception("Moron: not a chapter"))
				end_verse = len(chapters[end_chapter - 1])
			else:
				end_chapter, end_verse = map(try_nat, end.split(":"))
		else:
			start_chapter, start_verse = map(try_nat, start.split(":"))
			if ":" not in end:
				end_chapter = start_chapter
				end_verse = try_nat(end)
			else:
				(end_chapter, end_verse) = map(try_nat, end.split(":"))
	elif ":" not in str_:
		start_chapter = try_nat(str_)
		start_verse = 1
		end_chapter = start_chapter
		if start_chapter > len(chapters): raise(Exception("Moron: not a chapter"))
		end_verse = len(chapters[start_chapter - 1])
	else:
		start_chapter, start_verse = map(try_nat, str_.split(":"))
		end_chapter, end_verse = start_chapter, start_verse
	return start_chapter, start_verse, end_chapter, end_verse

def try_nat(str_):
	if str_ == "": raise(Exception("Moron: Empty int"))
	if not str_.isdigit(): raise(Exception("Moron: Not number"))
	return int(str_)

def get_passage_chunk(chapters, passage_chunk):
	start_chapter, start_verse, end_chapter, end_verse = passage_chunk
	if start_chapter > end_chapter: raise(Exception("Moron: wrong chapter order"))
	if start_chapter == end_chapter and start_verse > end_verse: raise(Exception("Moron: wrong verse order"))
	if start_chapter > len(chapters) or start_verse > len(chapters[start_chapter - 1]): raise(Exception("Moron: not in there"))
	if end_chapter > len(chapters) or end_verse > len(chapters[end_chapter - 1]): raise(Exception("Moron: not in there"))
	
	res = []
	
	for chapter in range(start_chapter - 1, end_chapter):
		verses = chapters[chapter]
		if start_chapter == end_chapter: verse_range = range(start_verse - 1, end_verse)
		elif chapter == 1: verse_range = range(start_verse - 1, len(verses))
		elif chapter == end_chapter - 1: verse_range = range(end_verse)
		else: verse_range = range(len(verses))
		
		chapter_res = []
		for verse in verse_range:
			chapter_res.append({"loc": f"{chapter+1}:{verse+1}", "text": verses[verse]})
		
		res.append({
			"section":
				f"{chapter+1}:{verse_range.start+1}-{verse_range.stop}"
				if start_chapter != end_chapter or start_verse != end_verse
				else f"{start_chapter}:{start_verse}",
			"verses": chapter_res
		})
	
	return res

def chapter_menu(book_name, passages):
	async def gen(_):
		print(passages[0])
		yield sum(map(lambda chapter: math.ceil(len(chapter["verses"]) / 5), passages))
		for chapter in passages:
			for chunk in utils.chunks(chapter["verses"], 5):
				yield verse_chunk_to_embed(f"{book_name} {chapter['section']}", chunk)
	return gen

def verse_chunk_to_embed(section, verses):
	embed = (discord.Embed(
		color = utils.embed_color)
		.set_author(
			name = section,
			icon_url = utils.icons["bible"]))
	for verse in verses:
		embed.add_field(name = verse["loc"], value = verse["text"], inline = False)
	return embed

def setup(client):
	client.add_cog(Bible(client))