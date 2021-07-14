import discord
from discord.ext import commands
import os
bot = commands.Bot(command_prefix="!")

token = os.environ["Discord_token"]

bot.load_extension("cog.server")

bot.run(token)
