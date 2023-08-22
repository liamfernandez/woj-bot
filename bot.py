# bot.py
import os
from typing import List
import discord
from discord.ext import commands
from dotenv import load_dotenv

# 1
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 2
intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix="/")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!\n\n")
    for guild in bot.guilds:
        print(
            f"Name of server: {guild.name}, members in the league: {guild.member_count}"
        )
        for member in guild.members:
            print(f"{member.name}")


@bot.command(name="report-a-trade", help="Report a trade to the rest of the league.")
async def wojBomb(
    ctx, team1: str, team2: str, team1Receives: List[str], team2Receives: List[str]
):
    await ctx.send(response)


bot.run(TOKEN)
