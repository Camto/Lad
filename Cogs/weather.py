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
		url = f"http://api.openweathermap.org/data/2.5/weather?appid=64dfdf86422ef9ce4e4763229c6f15e8&q={cityName}"
		response = requests.get(url)
		weather = response.json()
		channel = ctx.message.channel

		if weather["cod"] != "404":
			async with channel.typing():
				info = weather["main"]
				temperature = info["temp"]
				temperatureC = round(temperature - 273.15)
				temperatureF = str(round(temperatureC * 9/5) + 32)
				cPressure = info["pressure"]
				cHumidity = info["humidity"]
				w = weather["weather"]
				country = weather["sys"]["country"]
				timezone = weather["timezone"]
				weatherDescription = w[0]["description"]

				embed = discord.Embed(
					title = f"Weather in {cityName}",
					color = utils.embed_color,
					timestamp = ctx.message.created_at)
					.set_footer(
					text = f"Requested by {ctx.author.name}#{ctx.author.discriminator}")
				
				embed.set_author(
					name = f"Weather in {cityName}", 
					icon_url = utils.icons["weather"])

				fields = [
					("Description", f"**{weatherDescription}**"),
					("Temperature(F)", f"**{temperatureF}°F**"), 
					("Temperature(C)", f"**{str(temperatureC)}°C**"),
					("Humidity(%)", f"**{cHumidity}%**"),
					("Atmospheric Pressure(hPa)", f"**{cPressure}hPa**"),
					("Country", f"**{country}**"),
					("Timezone", f"**{timezone}**")
				]

				for name, value in fields:
					embed.add_field(name = name, value = value, inline = False)

			await channel.send(embed = embed)

		else:
			await channel.send(embed = discord.Embed(
				title = "City not found :x:", 
				color = utils.embed_color))

def setup(client):
	client.add_cog(Weather(client))