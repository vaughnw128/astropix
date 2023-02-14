import bs4 as bs
import urllib
import discord
from config import token, guild, channel
import aiohttp
import io
from os import sys

# Sets the guild
MY_GUILD = discord.Object(id=int(guild))

# Initializes the client
class MyClient(discord.Client):
    # Says it's ready and gets the channel and guild, then sends the formatted messages and crashes itself (POG!)
    async def on_ready(self):
        print('Bot online!')
        self.guild = self.get_guild(int(guild))
        self.channel = self.guild.get_channel(int(channel))
        print(f"Guild: {self.guild}")
        print(f"Channel: {self.channel}")
        
        # Uses bs4 to get the page, it shouldn't change (I hope?)
        html_page = urllib.request.urlopen("https://apod.nasa.gov/apod/astropix.html")
        soup = bs.BeautifulSoup(html_page)
        images = []
        alt=""
        for img in soup.findAll('img', alt=True):
            images.append(img.get('src'))
            alt = img.get('alt')
        
        # Creates an aiohttp session and grabs the image and makes a discord.File object in order to send it properly, then crashes itself
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://apod.nasa.gov/{images[0]}") as resp:
                img = await resp.read()
                with io.BytesIO(img) as file:
                    await self.channel.send(content=f"Astronomy Picture of the Day!\n\n{alt}\n\nhttps://apod.nasa.gov/apod/astropix.html", file=discord.File(file, "astropic.jpg"))
                    await sys.exit()

# Runs the bot
client = MyClient(intents=discord.Intents.default())
client.run(token)
