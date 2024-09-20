import asyncio
import discord
import functions
import os
import random
import requests
import re
from discord.ext import tasks, commands
from discord import Interaction, User, TextChannel, Role, app_commands
from discord.ext import tasks, commands
from discord import Interaction, User, TextChannel, Role
from dotenv import load_dotenv

# Enable message content intent
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with proper intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        ratecheck.start()  # Start the background task
    except Exception as e:
        print(e)

@bot.command()
async def say(ctx, *, message: str):
    await ctx.send(message)

load_dotenv()
my_secret = os.environ['TOKEN']

# ASA Server search
server_url = 'https://cdn2.arkdedicated.com/servers/asa/officialserverlist.json'
rate_url = "https://cdn2.arkdedicated.com/asa/dynamicconfig.ini"

# Fetch the current ASA PVE rates
@bot.tree.command(name="rates", description="Current ASA Server Rates")
async def rates(interaction: discord.Interaction):
    rate = requests.get(rate_url).text
    pattern = r"^\s*([\w.]+)\s*=\s*([\w.-]+)\s*$"
    values = []
    for line in rate.split('\n'):
        match = re.match(pattern, line)
        if match:
            values.append(match.groups()[1])

    emb = discord.Embed(
        title='ASA Official Server Rates',
        description="",
        colour=discord.Colour.pink()
    )
    emb.set_thumbnail(url='https://ark.wiki.gg/images/thumb/0/0a/ASA_Logo_transparent.png/198px-ASA_Logo_transparent.png')
    emb.add_field(name=f"**✨ `{values[2]}x` EXP**", value='', inline=False)
    emb.add_field(name=f"**🌴 `{values[1]}x` Harvesting**", value='', inline=False)
    emb.add_field(name=f"**🦖 `{values[0]}x` Taming**", value='', inline=False)
    emb.add_field(name=f"**💞 `{values[3]}x` Mating Interval**", value='', inline=False)
    emb.add_field(name=f"**🐣 `{values[5]}x` Egg Hatch**", value='', inline=False)
    emb.add_field(name=f"**🐤 `{values[4]}x` Baby Mature**", value='', inline=False)
    emb.add_field(name=f"**🤗 `{values[7]}x` Imprint**", value='', inline=False)
    emb.add_field(name=f"**🤗 `{values[6]}x` Cuddle Interval**", value='', inline=False)
  
    await interaction.response.send_message(embed=emb)

# Server status command
@bot.tree.command(name="serverstatus", description="Checks the server status")
@app_commands.describe(server="Server Number")
async def serverstatus(interaction: discord.Interaction, server: str):
    await interaction.response.send_message(f"Searching for {server}\n-------------------------------")
    result = functions.find_server(server)
    await interaction.channel.send(result)

# Summon command
@bot.tree.command(name="summon", description="Summon a user via DM")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(to_user="User to summon")
async def summon(interaction: discord.Interaction, to_user: User):
    await to_user.create_dm()
    chan = interaction.channel
    await to_user.send(f"Your presence is requested in: {chan.mention}")
    await interaction.response.send_message(f"Message has been sent to {to_user.mention} successfully!", ephemeral=True)

# Summon command error handling
@summon.error
async def summon_error(interaction: discord.Interaction, error):
    await interaction.response.send_message("<a:alert:932990503258054677> You don't have permissions to use this command!", ephemeral=True)

# Rate check task loop (runs every 1 minute)
@tasks.loop(minutes=1)
async def ratecheck():
    serverlist, data, flag = functions.loop()
    if flag == 0:
        pattern = r"^\s*([\w.]+)\s*=\s*([\w.-]+)\s*$"
        values = []
        for line in data.split('\n'):
            match = re.match(pattern, line)
            if match:
                values.append(match.groups()[1])

        for ent in serverlist:
            try:
                guild = bot.get_guild(int(ent['server_id']))
                channel = guild.get_channel(int(ent['channel_id']))
                role = guild.get_role(int(ent['role']))
                emb = discord.Embed(
                    title='ASA Official Server Rates',
                    description="",
                    colour=discord.Colour.pink()
                )
                emb.set_thumbnail(url='https://ark.wiki.gg/images/thumb/0/0a/ASA_Logo_transparent.png/198px-ASA_Logo_transparent.png')
                emb.add_field(name=f"**✨ `{values[2]}x` EXP**", value='', inline=False)
                emb.add_field(name=f"**🌴 `{values[1]}x` Harvesting**", value='', inline=False)
                emb.add_field(name=f"**🦖 `{values[0]}x` Taming**", value='', inline=False)
                emb.add_field(name=f"**💞 `{values[3]}x` Mating Interval**", value='', inline=False)
                emb.add_field(name=f"**🐣 `{values[5]}x` Egg Hatch**", value='', inline=False)
                emb.add_field(name=f"**🐤 `{values[4]}x` Baby Mature**", value='', inline=False)
                emb.add_field(name=f"**🤗 `{values[7]}x` Imprint**", value='', inline=False)
                emb.add_field(name=f"**🤗 `{values[6]}x` Cuddle Interval**", value='', inline=False)
                await channel.send(embed=emb)
                await channel.send(f"{role.mention}")
            except KeyError:
                print("Server channel missing or something went wrong!")

bot.run(my_secret)