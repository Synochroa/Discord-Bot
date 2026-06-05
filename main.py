import discord
from discord.ext import commands
import asyncio
import sqlite3
import time
from collections import defaultdict
user_messages = defaultdict(list)

from dotenv import load_dotenv

import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    
    from dotenv import load_dotenv

    load_dotenv()

    TOKEN = os.getenv("TOKEN")
    
from datetime import timedelta

conn = sqlite3.connect("warnings.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS warnings (
    user_id INTEGER,
    reason TEXT
)
""")

conn.commit()

intents = discord.Intents.default()
intents.message_content = True
GUILD_ID = 1509153631256187012

class MyBot(commands.Bot):

    async def setup_hook(self):

        guild = discord.Object(id=GUILD_ID)

        bot.tree.copy_global_to(guild=guild)

        synced = await self.tree.sync(guild=guild)

        print(f"Synced {len(synced)} command(s)")
        
        for cmd in synced:
            print(cmd.name)


bot = MyBot(
    command_prefix="?s ",
    intents=intents
)

@bot.event
async def on_ready():
    
    print(f"Logged in as {bot.user}") 

#--------------------------------------------------------------------Cogs

async def load_extensions():

    await bot.load_extension(
        "cogs.fun"
    )

    await bot.load_extension(
        "cogs.moderation"
    )
#---------------------------------------------------------------AUTO MODERATION------------------------------------------------------------------------

Filtered = []

@bot.event
async def on_message(message):

    if message.author.bot:
        return


    current_time = time.time()

    user_messages[message.author.id].append(current_time)

    user_messages[message.author.id] = [
        t for t in user_messages[message.author.id]
        if current_time - t < 10
    ]

    if len(user_messages[message.author.id]) >= 7:

        await message.author.timeout(
            timedelta(minutes=5),
            reason="spam detected"
        )

        embed = discord.Embed(
        title="Spam detected!",
        description=f"{message.author.mention} please avoid spamming in chat!",
        colour= discord.Color.red()
        )

        await message.channel.send(embed=embed)

        user_messages[message.author.id].clear()

        channel =bot.get_channel(1509206196500955257)

        await channel.send(f"{message.author.mention} is found guility of spamming!")

    if "discord.gg/" in message.content.lower():

        await message.delete()

        embed = discord.Embed(
        title="No advertising!",
        description=f"{message.author.mention} Please avoid advertising in channels!",
        color=discord.Color.red()
        )

        await message.channel.send(embed=embed)
    
    words = message.content.lower().split()

    for word in words:
        
        if word in Filtered:

            await message.delete()

            embed = discord.Embed(
            title="Filtered word found!",
            description=f"{message.author.mention} Please avoid using inappropriate language!",
            color=discord.Color.red()
            )

            await message.channel.send(embed=embed)

            break


    await bot.process_commands(message)

#--------------------------------------------------------------------

async def main():

    async with bot:

        await load_extensions()

        await bot.start(TOKEN)

asyncio.run(main())