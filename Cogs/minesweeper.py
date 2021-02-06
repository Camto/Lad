import discord
from discord.ext import commands
import utils

import random

class Minesweeper(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def minesweeper(self, ctx, *args):
		if len(args) == 0:
			width = 9
			height = 9
			mine_count = 10
		elif len(args) == 3 and all(map(lambda s: s.isnumeric(), args)):
			int_args = list(map(int, args))
			if any(map(lambda n: n < 1, int_args)):
				return await ctx.send(embed = utils.embeds["minesweeper error"])
			width, height, mine_count = int_args
		else:
			return await ctx.send(embed = utils.embeds["minesweeper error"])
		
		if (
				width > 40 or height > 40 or
				mine_count > width * height):
			return await ctx.send(embed = utils.embeds["minesweeper limits"])
		
		minesweeper_board = gen_minesweeper(width, height, mine_count)
		
		if len(minesweeper_board) > 2000:
			return await ctx.send(embed = utils.embeds["minesweeper char limit"])
		await ctx.send(minesweeper_board)

def gen_minesweeper(width, height, mine_count):
	board = [[0 for _ in range(width + 2)] for _ in range(height + 2)]
	
	possible_mines = [(x + 1, y + 1) for x in range(width) for y in range(height)]
	mines = random.sample(possible_mines, mine_count)
	for (x, y) in mines:
		for off_y in range(-1, 2):
			for off_x in range(-1, 2):
				board[y + off_y][x + off_x] += 1
	
	for (x, y) in mines:
		board[y][x] = -1
	
	num_to_emoji = lambda num: f"""||:{({
		-1: "bomb",
		0: "zero",
		1: "one",
		2: "two",
		3: "three",
		4: "four",
		5: "five",
		6: "six",
		7: "seven",
		8: "eight",
		9: "nine"
	})[num]}:||"""
	
	return "\n".join(map(lambda row: "".join(map(num_to_emoji, row[1:-1])), board[1:-1]))

def setup(client):
	client.add_cog(Minesweeper(client))