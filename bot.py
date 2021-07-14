import discord
from discord.ext import commands
bot = commands.Bot(command_prefix="!")

token = [token]

bot.load_extension("cog.server")

bot.run(token)
