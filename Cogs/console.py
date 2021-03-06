import discord
from discord.ext import commands
import utils

utils.master_settings["admins"] = list(map(int, utils.master_settings["admins"]))
utils.master_settings["console"] = int(utils.master_settings["console"])

import enum
import json
import asyncio
import ast
import aioconsole
import lark

# The master console!

class Console(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_ready(self):
		while True:
			cmd = ""
			last_line = await aioconsole.ainput()
			while len(last_line) > 0 and last_line[0] == "#":
				cmd += last_line[1:] + "\n"
				last_line = await aioconsole.ainput()
			cmd += last_line
			
			try:
				await run_cmd(self.client, cmd)
			except Exception as err:
				print(err)
	
	@commands.Cog.listener()
	async def on_message(self, msg):
		if (
				msg.channel.id == utils.master_settings["console"] and
				msg.author.id in utils.master_settings["admins"]):
			await run_cmd(self.client, msg.content, msg)
	
	@commands.command()
	async def ls(self, ctx, *, arg):
		if ctx.message.author.id in utils.master_settings["admins"]:
			await run_cmd(self.client, arg, ctx.message)

lad_script = lark.Lark(r"""
	start: WS? (action WS? (";" WS? action WS?)*)
	
	?action: msg
		| var
		| instrs
	
	msg: />.*/
	
	var: WS? CNAME WS? "=" WS? instrs
	
	instrs: WS? (instr WS?)*
	
	?instr: op
		| CNAME -> name
		| ref
		| eval
		| path
		| discord_obj
		| INT -> int
		| FLOAT -> float
		| word_string
		| ESCAPED_STRING -> string
		| store
		| func
	
	?op: "[" -> list_start
		| "{" -> obj_start
		| /\]|}|,/ -> list_or_obj_cont
		| ":" -> obj_sep
	
	ref: "\\" CNAME
	
	eval: /```([^`]|`(?!``))*```/
	
	?path: /\.+(\/[^ \n]+)?/ -> plain_path
		| "/" ESCAPED_STRING -> quoted_path
	
	?discord_obj: mention
		| emoji
		| channel
		| role
	
	mention: "<@!" INT ">" -> discord_mention
		| "@" ESCAPED_STRING -> search_mention
	
	emoji: /<a?:[A-Za-z0-9_]+:/ INT ">" -> discord_emoji
	
	channel: "<#" INT ">" -> discord_channel
	
	role: "<@&" INT ">" -> discord_role
	
	word_string: "'" CNAME
	
	store: "->" CNAME
	
	func: "(" start ")"
	
	ESCAPED_STRING: /"([^"\\]|(\\.))*"/
	
	%import common.CNAME
	%import common.WS
	%import common.INT
	%import common.FLOAT""")

class Types():
	(
		msg, var, instrs,
		name, ref, int, float, string, path,
		mention, emoji, channel, role,
		store, eval, func,
		list_start, obj_start, list_or_obj_cont
	) = (
		"msg", "var", "instrs",
		"name", "ref", "int", "float", "string", "path",
		"mention", "emoji", "channel", "role",
		"store", "eval", "func",
		"list_start", "obj_start", "list_or_obj_cont"
	)

def lad_script_transformer(client, msg):
	class Lad_Script_Transformer(lark.Transformer):
		start = lambda self, as_: list(filter(lambda a: a is not None, as_))
		msg = lambda self, m: {"type": Types.msg, "msg": m[0][2:]}
		def var(self, v):
			v = list(filter(lambda t: t is not None, v))
			return {"type": Types.var, "name": v[0].lower().replace("_", ""), "def": [v[1]]}
		instrs = lambda self, is_: {"type": Types.instrs, "instrs": list(filter(lambda i: i is not None, is_))}
		list_start = lambda self, _: {"type": Types.list_start}
		obj_start = lambda self, _: {"type": Types.obj_start}
		list_or_obj_cont = lambda self, _: {"type": Types.list_or_obj_cont}
		obj_sep = lambda self, _: None
		name = lambda self, n: {"type": Types.name, "name": n[0].lower().replace("_", "")}
		ref = lambda self, r: {"type": Types.ref, "name": r[0].lower().replace("_", "")}
		int = lambda self, n: {"type": Types.int, "int": int(n[0])}
		float = lambda self, n: {"type": Types.float, "float": float(n[0])}
		string = lambda self, s: {"type": Types.string, "string": eval(s[0])}
		eval = lambda self, e: {"type": Types.eval, "eval": remove_prefix(remove_prefix(e[0][3:-3], "py"), "thon")}
		plain_path = lambda self, p: {"type": Types.path, "path": p[0]}
		quoted_path = lambda self, p: {"type": Types.path, "path": p[0][1:-1]}
		discord_mention = lambda self, m: {"type": Types.mention, "mention": int(m[0])}
		search_mention = lambda self, m: {"type": Types.mention, "mention": 0 if True else m[0][1:-1]}
		# Add is_animated prop for proper rendering
		discord_emoji = lambda self, e: {"type": Types.emoji, "emoji": int(e[1])}
		discord_channel = lambda self, c: {"type": Types.channel, "channel": int(c[0])}
		discord_role = lambda self, r: {"type": Types.role, "role": int(r[0])}
		word_string = lambda self, s: {"type": Types.string, "string": s[0]}
		store = lambda self, s: {"type": Types.store, "name": s[0].lower().replace("_", "")}
		func = lambda self, f: {"type": Types.func, "body": f[0]}
		WS = lambda self, _: None
	return Lad_Script_Transformer()

st = []
vars = utils.get_json("../Console/vars")
aliases = utils.get_json("../Console/aliases")
g = globals()

async def run_cmd(client, cmd, msg = None):
	actions = lad_script_transformer(client, msg).transform(lad_script.parse(cmd))
	print(actions)
	await run(client, msg, actions, [])

async def run(client, msg, actions, locals_):
	for action in actions:
		if action["type"] == Types.msg:
			if "channel" in vars:
				if type(vars["channel"]) == int:
					channel = client.get_channel(vars["channel"])
					if action["msg"] != "":
						await channel.send(action["msg"])
					elif len(st) >= 1:
						msg = st.pop()
						if type(msg) == str:
							await channel.send(msg)
				else:
					print("Invalid type for channel.")
		elif action["type"] == Types.var:
			await run(client, msg, action["def"], locals_)
			if action["name"] in aliases:
				vars[aliases[action["name"]]] = st.pop()
			else:
				vars[action["name"]] = st.pop()
		else:
			for instr in action["instrs"]:
				if instr["type"] == Types.name:
					local = list(filter(lambda l: l[0] == instr["name"], locals_))
					if local:
						var = local[0][1]
					elif instr["name"] in aliases:
						var = vars[aliases[instr["name"]]]
					elif instr["name"] in vars:
						var = vars[instr["name"]]
					else:
						print(f"Variable {instr['name']} not found.")
						break
					
					if type(var) != dict or var["type"] != Types.func:
						st.append(var)
					else:
						await run(client, msg, var["body"], locals_)
				elif instr["type"] == Types.ref:
					local = list(filter(lambda l: l[0] == instr["name"], locals_))
					if local:
						var = local[0][1]
					elif instr["name"] in aliases:
						var = vars[aliases[instr["name"]]]
					elif instr["name"] in vars:
						var = vars[instr["name"]]
					else:
						print(f"Variable {instr['name']} not found.")
						break
					
					st.append(var)
				elif instr["type"] == Types.int:
					st.append(int(instr["int"]))
				elif instr["type"] == Types.float:
					st.append(instr["float"])
				elif instr["type"] == Types.string:
					st.append(str(instr["string"]))
				elif instr["type"] in [Types.mention, Types.emoji, Types.channel, Types.role]:
					st.append(instr)
				elif instr["type"] in [Types.path, Types.func]:
					st.append(instr)
				elif instr["type"] == Types.eval:
					await aexec(instr["eval"], dict(globals(), **locals()))
				elif instr["type"] == Types.list_start:
					st.append([])
				elif instr["type"] == Types.obj_start:
					st.append({})
				elif instr["type"] == Types.list_or_obj_cont:
					item = st.pop()
					ls_or_key = st.pop()
					if type(ls_or_key) == list:
						st.append(ls_or_key + [item])
					else:
						obj = st.pop().copy()
						obj[ls_or_key] = item
						st.append(obj)

async def aexec(stmts, env = None):
	parsed_stmts = ast.parse(stmts)
	
	fn = f"async def async_fn(): pass"
	parsed_fn = ast.parse(fn)
	
	for node in parsed_stmts.body:
		ast.increment_lineno(node)
	
	parsed_fn.body[0].body = parsed_stmts.body
	exec(compile(parsed_fn, filename = "<ast>", mode = "exec"), env)
	
	return await eval(f"async_fn()", env)

def remove_prefix(text, prefix):
	if text.startswith(prefix):
		return text[len(prefix):]
	return text

def setup(client):
	client.add_cog(Console(client))