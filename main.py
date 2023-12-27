import discord
import search_leetcode
from datetime import datetime
from discord.ext import tasks
import asyncio

# instantiate discord client 
intents = discord.Intents(messages=True, guilds = True)
intents.message_content = True
client = discord.Client(intents = intents)

channel_id = 698981558232809493 #932232214391959604 
role_id =  757266745697370185 #1039988519210332281
runtime = "09:00"




@client.event
async def on_ready():
  print("bot:user ready == {0.user}".format(client))
  current_time = datetime.now().strftime("%H:%M")
  while ( not current_time == runtime):
    current_time = datetime.now().strftime("%H:%M")
    await asyncio.sleep(1)

  if not myLoop.is_running():
    myLoop.start()

        
  
@tasks.loop(hours=24)
async def myLoop():
  #print("bot:user ready == {0.user}".format(client))
  channel = client.get_channel(channel_id)
  #print(channel)
  result = search_leetcode.getQuestionDeets()
  await channel.send(f"<@&{role_id}> {result[0]} \n {result[2]} \n {result[1]}")



client.run("MTAzNzQ4OTExODg1NjM2MDA1Nw.GFYPNF.PDv2bejDm5jW_mZMQ4XvbyglIAeadFxnUm8qnk")