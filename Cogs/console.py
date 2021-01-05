import discord
from discord.ext import commands
import utils

import enum
import json
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
			
			await run_cmd(self.client, cmd)
	
	@commands.Cog.listener()
	async def on_message(self, msg):
		if (
				msg.channel.id == utils.master_settings["console"] and
				msg.author.id in utils.master_settings["admins"]):
			cmd = msg.content
			await run_cmd(self.client, cmd)

lad_script = lark.Lark(r"""
	start: WS? (action WS? (";" WS? action WS?)*)
	
	?action: msg
		| var
		| instrs
	
	msg: />.*/
	
	var: WS? WORD WS? "=" WS? instrs
	
	instrs: WS? (instr WS?)*
	
	?instr: WORD -> name
		| ref
		| eval
		| path
		| mention
		| INT -> int
		| FLOAT -> float
		| word_string
		| ESCAPED_STRING -> string
		| store
		| func
	
	ref: "\\" WORD
	
	eval: /```([^`]|`(?!``))*```/
	
	?path: /\.+(\/[^ \n]+)?/ -> plain_path
		| "/" ESCAPED_STRING -> quoted_path
	
	mention: "@" ESCAPED_STRING
	
	word_string: "'" WORD
	
	store: "->" WORD
	
	func: "(" start ")"
	
	ESCAPED_STRING: /"([^"\\]|(\\.))*"/
	
	%import common.WORD
	%import common.WS
	%import common.INT
	%import common.FLOAT""")

class Types(enum.Enum):
	(
		actions,
		msg, var, instrs,
		name, ref, int, float, string, path, mention,
		store, eval, func
	) = range(14)

class Lad_Script_Transformer(lark.Transformer):
	start = list
	msg = lambda self, m: {"type": Types.msg, "msg": m[0][1:]}
	var = lambda self, v: {"type": Types.var, "name": v[0].lower().replace("_", ""), "def": [v[3]]}
	instrs = lambda self, is_: {"type": Types.instrs, "instrs": list(filter(lambda i: i is not None, is_))}
	name = lambda self, n: {"type": Types.name, "name": n[0].lower().replace("_", "")}
	ref = lambda self, r: {"type": Types.ref, "name": r[0].lower().replace("_", "")}
	int = lambda self, n: {"type": Types.int, "int": int(n[0])}
	float = lambda self, n: {"type": Types.float, "float": float(n[0])}
	string = lambda self, s: {"type": Types.string, "string": s[0]}
	eval = lambda self, e: {"type": Types.eval, "eval": e[0][3:-3]}
	plain_path = lambda self, p: {"type": Types.path, "path": p[0]}
	quoted_path = lambda self, p: {"type": Types.path, "path": p[0][1:-1]}
	mention = lambda self, m: {"type": Types.mention, "mention": p[0][1:-1]}
	word_string = lambda self, s: {"type": Types.string, "string": s[0]}
	store = lambda self, s: {"type": Types.store, "name": s[0].lower().replace("_", "")}
	func = lambda self, f: {"type": Types.func, "body": f[0]}
	WS = lambda self, _: None

st = []
vars = utils.get_json("../Console/vars")
aliases = utils.get_json("../Console/aliases")

async def run_cmd(client, cmd):
	actions = Lad_Script_Transformer().transform(lad_script.parse(cmd))
	print(actions)
	await run(client, actions, [])

async def run(client, actions, locals):
	for action in actions:
		if action["type"] == Types.msg:
			if "channel" in vars:
				channel = client.get_channel(vars["channel"])
				if action["msg"] != "":
					await channel.send(action["msg"])
				elif len(st) >= 1:
					msg = st.pop()
					if type(msg) == str:
						await channel.send(msg)
		elif action["type"] == Types.var:
			await run(client, action["def"], locals)
			vars[action["name"]] = st.pop()
			print(vars)
		else:
			for instr in action["instrs"]:
				if instr["type"] == Types.name:
					local = list(filter(lambda l: l[0] == instr["name"], locals))
					if local:
						var = local[0][1]
					elif instr["name"] in vars:
						var = vars[instr["name"]]
					else:
						print(f"Variable {instr['name']} not found.")
						continue
					
					if type(var) != dict or var["type"] != Types.func:
						st.append(var)
					else:
						await run(client, var["body"], locals)
				elif instr["type"] == Types.ref:
					local = list(filter(lambda l: l[0] == instr["name"], locals))
					if local:
						var = local[0][1]
					elif instr["name"] in vars:
						var = vars[instr["name"]]
					else:
						print(f"Variable {instr['name']} not found.")
						continue
					
					st.append(var)
				elif instr["type"] == Types.int:
					st.append(int(instr["int"]))
				elif instr["type"] == Types.float:
					st.append(instr["float"])
				elif instr["type"] == Types.string:
					st.append(instr["string"])
				elif instr["type"] in [Types.path, Types.mention, Types.func]:
					st.append(instr)
				elif instr["type"] == Types.eval:
					eval(instr["eval"])

def setup(client):
	client.add_cog(Console(client))