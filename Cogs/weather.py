import discord
from discord.ext import commands
import utils

import requests

class Weather(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def weather(self, ctx, *, city: str):
		city_name = city
		url = f"http://api.openweathermap.org/data/2.5/weather?appid=64dfdf86422ef9ce4e4763229c6f15e8&q={city_name}"
		response = requests.get(url)
		weather = response.json()
		channel = ctx.message.channel
		
		if weather["cod"] != "404":
			async with channel.typing():
				info = weather["main"]
				temperature = info["temp"]
				temperature_c = round(temperature - 273.15)
				temperature_f = round(temperature_c * 9/5) + 32
				pressure = info["pressure"]
				humidity = info["humidity"]
				w = weather["weather"]
				country = weather["sys"]["country"]
				timezone = weather["timezone"]
				weather_description = w[0]["description"]
				
				embed = (discord.Embed(
					color = utils.embed_color,
					timestamp = ctx.message.created_at)
					.set_footer(
						text = f"Requested by {ctx.author.name}#{ctx.author.discriminator}"))
				
				embed.set_author(
					name = f"Weather in {city_name}", 
					icon_url = utils.icons["weather"])
				
				fields = [
					("Description", f"**{weather_description}**"),
					("Temperature(F)", f"**{temperature_f}°F**"), 
					("Temperature(C)", f"**{temperature_c}°C**"),
					("Humidity(%)", f"**{humidity}%**"),
					("Atmospheric Pressure(hPa)", f"**{pressure}hPa**"),
					("Country", f"**{country}**"),
					("Timezone", f"**{timezone}**")
				]
				
				for name, value in fields:
					embed.add_field(name = name, value = value, inline = False)
				
				await channel.send(embed = embed)
		
		else:
			await channel.send(embed = discord.Embed(
				color = utils.embed_color)
				.set_author(
					name = f':x: City *{city_name}* not found',
					icon_url = utils.icons["weather"]))

def setup(client):
	client.add_cog(Weather(client))