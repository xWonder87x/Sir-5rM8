import asyncio
import discord
import functions
import os
import json
import subprocess
import random
import requests
import re
from discord.ext import commands
from discord import Interaction
from discord import app_commands
from discord.utils import get
from discord import User
from datetime import datetime
from datetime import timedelta
from discord import TextChannel,Role
from dotenv import load_dotenv

#from dotenv import load_dotenv
load_dotenv()
my_secret = os.environ['TOKEN']


bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

# ASA Server search
server_url = 'https://cdn2.arkdedicated.com/servers/asa/officialserverlist.json'



    
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
        
#server Rate command
rate_url="https://cdn2.arkdedicated.com/asa/dynamicconfig.ini"

@bot.tree.command(name="rates", description="Ark Official server Rates")
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
     title= 'Ark ascended Official server Rates',
     description="",
     colour=discord.Colour.pink()
   )
  emb.set_thumbnail(url=f"{img}")
  emb.add_field(
     name=keys[0]+' = '+values[0],
     value='',
     inline=False
  )
  emb.add_field(
     name=keys[1]+' = '+values[1],
     value='',
     inline=False
  )
  emb.add_field(
     name=keys[2]+' = '+values[2],
     value='',
     inline=False
  )
  emb.add_field(
     name=keys[3]+' = '+values[3],
     value='',
     inline=False
  )
  emb.add_field(
     name=keys[4]+' = '+values[4],
     value='',
     inline=False
  )
  emb.add_field(
     name=keys[5]+' = '+values[5],
     value='',
     inline=False
  )
  emb.add_field(
     name=keys[6]+' = '+values[6],
     value='',
     inline=False
  )
  emb.add_field(
     name=keys[7]+' = '+values[7],
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
async def ratecheck():
   serverlist,data,flag=functions.loop()
   if flag==0:
      pattern = r"^\s*([\w.]+)\s*=\s*([\w.-]+)\s*$"
      keys = []
      values = []
      img=bot.application.icon
      for line in data.split('\n'):
         match = re.match(pattern, line)
         if match:
            key, value= match.groups()
            keys.append(key)
            values.append(value)
   
      for ent in serverlist:
         try:
            guild=bot.get_guild(int(ent['server_id']))
            channel=guild.get_channel(int(ent['channel_id']))
            role=guild.get_role(int(ent['role']))   
            emb=discord.Embed(
            title= 'ASA Official PVE Server Rates',
            description=(f"**{keys[0]}** = {values[0]}\n**{keys[1]}** = {values[1]} \n**{keys[2]}** = {values[2]}\n**{keys[3]}** = {values[3]}\n**{keys[4]}** = {values[4]}\n**{keys[5]}** = {values[5]}\n**{keys[6]}** = {values[6]}\n**{keys[7]}** = {values[7]}"),
            colour=discord.Colour.pink()
            )
            emb.set_thumbnail(url=f"{img}")
            await channel.send(embed=emb)
            await channel.send(f"{role.mention}")
         except KeyError:
            print("Server channel missing or went something wrong!")
      await asyncio.sleep(300)  # 300 seconds = 5 minutes
      await ratecheck()

@bot.tree.command(name="set_rate_channel",description="set channel for rate updates")
@app_commands.describe(channel="channel")
@app_commands.describe(role="role")
@app_commands.checks.has_permissions(administrator=True)
async def set_rate_channel(int:discord.Integration,channel:TextChannel,role:Role):
   functions.add_server_channel(str(int.guild.id),str(channel.id),str(role.id))
   await channel.send("This channel is been set for automatic Official PVE rates updates.")
   await int.response.send_message(f"{channel.mention} is set for automatic Official PVE rates updates.")

@bot.tree.error
async def on_app_commandError(int:discord.Interaction,error):
   await int.response.send_message(error,ephemeral=True)


bot.run(my_secret)