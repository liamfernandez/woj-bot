# bot.py
import os
import discord
from dotenv import load_dotenv

# 1
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 2
intents = discord.Intents.default()
bot = commands.Bot(intents=intents, command_prefix="/")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


bot.run(TOKEN)
