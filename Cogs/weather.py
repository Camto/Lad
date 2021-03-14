import discord
from discord.ext import commands
import utils

import requests

class Weather(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def weather(self, ctx, *, city: str):
		cityName = city
		url = "http://api.openweathermap.org/data/2.5/weather?" + "appid=" + "64dfdf86422ef9ce4e4763229c6f15e8" + "&q=" + cityName
		response = requests.get(url)
		weather = response.json()
		channel = ctx.message.channel

		if isinstance(error, commands.MissingRequiredArgument):
			if error.param.name == "city":
				await ctx.send(embed = discord.Embed(title = "Please input a City name"))

		else:
			if weather["cod"] != "404":
				async with channel.typing():
					info = weather["main"]
					temperature = info["temp"]
					temperatureC = round(temperature - 273.15)
					temperatureF = str(round(temperatureC * 9/5) + 32)
					cPressure = info["pressure"]
					cHumidity = info["humidity"]
					w = weather["weather"]
					weatherDescription = w[0]["description"]

					embed = discord.Embed(
						title = f"Weather in {cityName}",
						color = utils.embed_color,
						timestamp = ctx.message.created_at
					)

					embed.add_field(name = "Description", value = f"**{weatherDescription}**", inline = False)
					embed.add_field(name = "Temperature(F)", value = f"**{temperatureF}°F**", inline = False)
					embed.add_field(name = "Temperature(C)", value = f"**{str(temperatureC)}°C**", inline = True)
					embed.add_field(name = "Humidity(%)", value = f"**{cHumidity}%**", inline = False)
					embed.add_field(name = "Atmospheric Pressure(hPa)", value = f"**{cPressure}hPa**", inline = False)
					embed.set_thumbnail(url = "https://raw.githubusercontent.com/Camto/Lad/master/Images/weather.png")
					embed.set_footer(text = f"Requested by {ctx.author.name}#{ctx.author.discriminator}")

				await channel.send(embed = embed)

			else:
				await channel.send(embed = discord.Embed(
					title = "City not found :x:", 
					color = utils.embed_color))

def setup(client):
	client.add_cog(Weather(client))