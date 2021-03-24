import discord
from discord.ext import commands
import utils

import math
import itertools
import re
import random

from fuzzywuzzy import fuzz, process

bible = utils.get_json("bible")
book_names = list(map(lambda book: book["name"], bible))

search_chars = re.compile("[^A-Za-z0-9:\-;]")
book_name_parse = re.compile("\d?[A-Za-z]+")

# Starting the bible study.
class Bible(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def bible(self, ctx, *, args = None):
		if utils.get_setting(ctx.guild, "bible"):
			if args == None:
				await utils.menus.reload(self.client, ctx, random_passage_menu())
			else:
				try:
					args = search_chars.sub("", args)
					book_name_match = book_name_parse.match(args)
					if book_name_match:
						book_name = book_name_match.group(0)
						args = args[book_name_match.end():]
					else: raise(Exception(utils.embeds["bible no book"]))
					
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
					await ctx.send(embed = e.args[0])
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
				if end_chapter > len(chapters): raise(Exception(invalid_chapter_embed(end_chapter)))
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
		if start_chapter > len(chapters): raise(Exception(invalid_chapter_embed(end_chapter)))
		end_verse = len(chapters[start_chapter - 1])
	else:
		start_chapter, start_verse = map(try_nat, str_.split(":"))
		end_chapter, end_verse = start_chapter, start_verse
	return start_chapter, start_verse, end_chapter, end_verse

def try_nat(str_):
	if str_ == "": raise(Exception(not_number_embed(str_)))
	if not str_.isdigit(): raise(Exception(not_number_embed(str_)))
	return int(str_)

def get_passage_chunk(chapters, passage_chunk):
	start_chapter, start_verse, end_chapter, end_verse = passage_chunk
	if start_chapter > end_chapter: raise(Exception(utils.embeds["bible wrong chapter order"]))
	if start_chapter == end_chapter and start_verse > end_verse: raise(Exception(utils.embeds["bible wrong verse order"]))
	if start_chapter == 0 or start_chapter > len(chapters): raise(Exception(invalid_chapter_embed(start_chapter)))
	if end_chapter == 0 or end_chapter > len(chapters): raise(Exception(invalid_chapter_embed(end_chapter)))
	if start_verse == 0 or end_verse == 0: raise(Exception(invalid_verse_embed(start_verse)))
	if start_verse > len(chapters[start_chapter - 1]): raise(Exception(invalid_verse_embed(start_verse)))
	if end_verse > len(chapters[end_chapter - 1]): raise(Exception(invalid_verse_embed(end_verse)))
	
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

def invalid_chapter_embed(chapter):
	return (discord.Embed(
		description = f"{chapter} isn't a chapter in this book.",
		color = utils.embed_color)
		.set_author(
			name = "Invalid Chapter",
			icon_url = utils.icons["bible"]))

def invalid_verse_embed(verse):
	return (discord.Embed(
		description = f"{verse} isn't a verse in this book.",
		color = utils.embed_color)
		.set_author(
			name = "Invalid Verse",
			icon_url = utils.icons["bible"]))

def not_number_embed(n):
	return (discord.Embed(
		description = f'"{n}" is not a valid number',
		color = utils.embed_color)
		.set_author(
			name = "Invalid Number",
			icon_url = utils.icons["bible"]))

def chapter_menu(book_name, passages):
	async def gen(_):
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