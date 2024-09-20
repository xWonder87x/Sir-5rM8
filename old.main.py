import asyncio
import discord
import functions
import os
import json
import subprocess
import random
import requests
import re
#added import tasks to handle automatic syncing for rates 
from discord.ext import tasks
from discord.ext import commands
from discord import Interaction
from discord import app_commands
from discord.utils import get
from discord import User
from datetime import datetime
from datetime import timedelta
from discord import TextChannel,Role
from dotenv import load_dotenv


# Enable message content intent
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with proper intents

bot = commands.Bot(command_prefix='!', intents=intents)

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


#bot.run('YOUR_BOT_TOKEN')


#from dotenv import load_dotenv
load_dotenv()
my_secret = os.environ['TOKEN']


#bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

# ASA Server search
server_url = 'https://cdn2.arkdedicated.com/servers/asa/officialserverlist.json'

#server Rate command
rate_url="https://cdn2.arkdedicated.com/asa/dynamicconfig.ini"

    
@bot.event
async def on_ready():
  print('We have logged in as {0.user}')
  try:
     synced = await bot.tree.sync()
     print(f"Synced {len(synced)} command(s)")
     await ratecheck()
     #functions.sfile()
  except Exception as e:
      print(e)


#Fetch the current ASA PVE rates
@bot.tree.command(name="rates", description="Current ASA Server Rates")
async def rates(int: discord.Interaction):
  rate=requests.get(rate_url).text
  config_data = {}
  pattern = r"^\s*([\w.]+)\s*=\s*([\w.-]+)\s*$"
  keys = []
  values = []
  img=int.client.application.icon
  for line in rate.split('\n'):
        match = re.match(pattern, line)
        if match:
            key, value = match.groups()
            keys.append(key)
            values.append(value)
  
  emb=discord.Embed(
     title= 'ASA Official Server Rates',
     description="",
     colour=discord.Colour.pink()
   )
  emb.set_thumbnail(url='https://ark.wiki.gg/images/thumb/0/0a/ASA_Logo_transparent.png/198px-ASA_Logo_transparent.png')
  emb.add_field(
      name=f"**✨ `{values[2]}x` EXP**",
      value='',
      inline=False
   )
  emb.add_field(
     name=f"**🌴 `{values[1]}x` Harvesting**",
     value='',
     inline=False
  )
  emb.add_field(
     name=f"**🦖 `{values[0]}x` Taming**",
     value='',
     inline=False
  )
  emb.add_field(
     name=f"**💞 `{values[3]}x` Mating Interval**",
     value='',
     inline=False
  )
  emb.add_field(
     name=f"**🐣 `{values[5]}x` Egg Hatch**",
     value='',
     inline=False
  )
  emb.add_field(
     name=f"**🐤 `{values[4]}x` Baby Mature**",
     value='',
     inline=False
  )
  emb.add_field(
     name=f"**🤗 `{values[7]}x` Imprint**",
     value='',
     inline=False
  )
  emb.add_field(
     name=f"**🤗 `{values[6]}x` Cuddle Interval**",
     value='',
     inline=False
  )
  
  await int.response.send_message(embed=emb)

    
#server status command
@bot.tree.command(name="serverstatus", description="Checks the server status")
@app_commands.describe(server="Server Number")
async def serverstatus(int: discord.Interaction,server:str):
   await int.response.send_message(f"Searching for {server}\n-------------------------------")
   result=functions.find_server(server)
   await int.channel.send(result)


#Sends a DM to summon the selected user
@bot.tree.command(name="summon", description="Summon a user via DM")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(to_user= "User to summon")
async def summon(int: discord.Interaction, to_user: User):
  if app_commands.checks.has_role(910297104105209916):
    await to_user.create_dm()
    chan=int.channel
    await to_user.send(f"Your presence is requested in: {chan.mention}")
    await int.response.send_message(f"Message has been sent to {to_user.mention} succesfully!",ephemeral=True)

@summon.error
async def summon_error(interaction: discord.Interaction, error):
  await interaction.response.send_message("<a:alert:932990503258054677> You don't have permissions to use this command!",ephemeral=True)


#Sends a DM to the selected user asking them to give us a feedback
@bot.tree.command(name="feedback", description="Requests a user to leave a feedback")
@app_commands.checks.has_role(910297104105209916)
@app_commands.describe(to_user= "User to send the request")
async def feedback(int: discord.Interaction, to_user: User):
  if app_commands.checks.has_role(910297104105209916):
    await to_user.create_dm()
    chan=int.channel
    await to_user.send(f"Did you enjoy the transaction with us? \nIt will be really helpful if you leave us a feedback.<a:wonderheart:944267237290819584>.\n<#755214742901227581>")
    await int.response.send_message(f"Message has been sent to {to_user.mention} succesfully!",ephemeral=True)

@feedback.error
async def feedback_error(interaction: discord.Interaction, error):
  await interaction.response.send_message("<a:alert:932990503258054677> Action failed, or you don't have permissions to use this command!",ephemeral=True)


msgs=["msassage0","msassage1","msassage2","msassage3","msassage4","msassage5","msassage6","msassage7","msassage8","msassage9"]
@bot.tree.command(name="show_tips",description="show tips")
async def show_tips(int:discord.Integration):
   msg=random.choice(msgs)
   await int.response.send_message(f"tips",ephemeral=True )
   await int.channel.send(f"{msg}")

#autoreply to keywords
#@bot.event
#async def on_message(message):
#    if message.content.lower()=='price':
#        embed = discord.Embed(title="<:wonderinfo:950154988301193216>  Important information", description="*Please include a price to your posts, if #not, they will be deleted.*", color=0xFF119A)
#        await message.channel.send(embed=embed)
#        await message.delete()
#    elif message.content.startswith('coffee'):
#        await message.reply('Here, I have a cup for you ☕ !', mention_author=True)



#intervel rates check
#tasks.loop ensures that the loop is running every x minutes
@tasks.loop(minutes=1)
async def ratecheck():
    # Add your existing ratecheck code here
    serverlist, data, flag = functions.loop()
    if flag == 0:
        pattern = r"^\s*([\w.]+)\s*=\s*([\w.-]+)\s*$"
        keys = []
        values = []
        img = bot.application.icon
        for line in data.split('\n'):
            match = re.match(pattern, line)
            if match:
                key, value = match.groups()
                keys.append(key)
                values.append(value)

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
                emb.set_thumbnail(url=f"{img}")
                await channel.send(embed=emb)
                await channel.send(f"{role.mention}")
            except KeyError:
                print("Server channel missing or something went wrong!")

@bot.tree.command(name="set_rate_channel",description="Choose a channel for official rate auto updates")
@app_commands.describe(channel="channel")
@app_commands.describe(role="role")
@app_commands.checks.has_permissions(administrator=True)
async def set_rate_channel(int:discord.Integration,channel:TextChannel,role:Role):
   functions.add_server_channel(str(int.guild.id),str(channel.id),str(role.id))
   await channel.send("# This channel is been set for automatic Official Server rate updates.")
   await int.response.send_message(f"Automatic updates will now be send to {channel.mention} and members with the role <@&{role.id}> will get notified.")

@bot.tree.error
async def on_app_commandError(int:discord.Interaction,error):
   await int.response.send_message(error,ephemeral=True)


bot.run(my_secret)