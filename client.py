# from typing import List
import os
import discord
import requests
from discord import app_commands
from dotenv import load_dotenv
from io import BytesIO

# CONSTANTS
# og_URL = "https://og-woj-bomb.vercel.app/api/woj-bomb"
og_URL = "https://og-woj-bomb-lpod5xzoy-liamfernandez.vercel.app/api/woj-bomb"
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

GENERAL_CHANNEL_ID = 1142903027951489056
TRADE_LOG_CHANNEL_ID = (
    1143707162607099924  # right now is set to bot-trade-log channel as to avoid spam
)

# Initiate Intents object. Needed for client or bot instantiation
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

team_choices = [
    app_commands.Choice(name="Liam", value="ChillTown BC"),
    app_commands.Choice(name="Lok", value="Lok's team"),
    app_commands.Choice(name="Daniel", value="Daniel's team"),
    app_commands.Choice(name="AJ", value="AJ's team"),
    app_commands.Choice(name="Rags", value="Rags' team"),
    app_commands.Choice(name="Tim", value="Tim's team"),
    app_commands.Choice(name="Iván", value="Iván's team"),
    app_commands.Choice(name="Tyler", value="Tyler's team"),
    app_commands.Choice(name="Robbie", value="Robbie's team"),
]


@tree.command(
    name="woj-bomb",
    description="Have Woj break the news to the rest of the league of a trade that you've made.",
)
@app_commands.choices(
    team1=team_choices,
    team2=team_choices,
)
async def woj_bomb(
    interaction: discord.Interaction,
    team1: app_commands.Choice[str],
    team2: app_commands.Choice[str],
):
    if team1 is team2:
        await interaction.response.send_message(
            "You can't trade with yourself, dummy!", ephemeral=True
        )
        return

    # Call image gen API with teamnames as params
    parameterizedUrl = f"{og_URL}?team1={team1.name}&team2={team2.name}"
    print(parameterizedUrl)
    response = requests.get(url=parameterizedUrl)
    if response.status_code != 200:
        await interaction.response.send_message(
            "My Twitter is down mate, one moment.",
            ephemeral=True,
        )
        return
    else:
        image_data = BytesIO(response.content)
        image_file = discord.File(image_data, "woj_bomb.png")
        await interaction.response.send_message(
            "Thanks for the scoop, I've posted the 💣 | P.S. do you have Rachel Nichols #?",
            ephemeral=True,
        )
        target_channel = client.get_channel(TRADE_LOG_CHANNEL_ID)
        await target_channel.send("Woj Bomb!", file=image_file)
        return


@client.event
async def on_ready():
    await tree.sync()
    print("\n\nReady!")


client.run(TOKEN)


# app_commands.Argument(
#             name="team 1",
#             description="The first team involved in the trade",
#             type=str,
#             choices=[
#                 {"name": "Liam", "value": "ChillTown BC"},
#                 {"name": "Lok", "value": "<Lok's team name here>"},
#             ],
#         ),
#         app_commands.Option(
#             name="team 2",
#             description="The second team involved in the trade",
#             type=str,
#             choices=[
#                 {"name": "Liam", "value": "ChillTown BC (Liam)"},
#                 {"name": "Lok", "value": "<Lok's team name here> (Lok)"},
#             ],
#         ),
#         app_commands.Option(
#             name="team1Receives",
#             description="What team 1 receives from the trade",
#             type=str,
#         ),
#         app_commands.Option(
#             name="team2Receives",
#             description="What team 2 receives from the trade",
#             type=str,
#         ),
