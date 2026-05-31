import discord
from discord.ext import commands
import sqlite3
import time
from collections import defaultdict
user_messages = defaultdict(list)
from dotenv import load_dotenv
import os

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

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?s ", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
#----------------------------------------------------------------INTERACTIVE COMMANDS---------------------------------------------------------------------------
@bot.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = ", ".join(x.name for x in members) 
    embed = discord.Embed(
    title="That's harsh...",
    description=f"{slapped} was slapped for {reason}",
    color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@slap.error
async def slap_error(ctx, error):
    embed = discord.Embed(
    title="Wrong usage!",
    description=f"Usage: ?s slap @User (Reason)",
    color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def kiss(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    kissed = ", ".join(x.name for x in members)
    embed = discord.Embed(
    title="Someone's getting feisty",
    description=f"{kissed} was kissed for {reason}",
    color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@kiss.error
async def kiss_error(ctx, error):
    embed = discord.Embed(
    title="Wrong usage!",
    description=f"Usage: ?s kiss @User (Reason)",
    color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def marry(ctx, member: discord.Member):
    embed = discord.Embed(
    title="A newlywed just appeared~?",
    description=f"Congraluations on {ctx.author.mention} and {member.mention} marriage~!",
    color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@marry.error
async def kiss_error(ctx, error):
    embed = discord.Embed(
    title="Wrong usage!",
    description=f"Usage: ?s marry @User",
    color=discord.Color.red()
    )
    await ctx.send(embed=embed)



#----------------------------------------------------------------MODERATION COMMANDS--------------------------------------------------------------------------------

@bot.command()
@commands.has_permissions(manage_messages=True)

async def clear(ctx, amt: int):
    await ctx.channel.purge(limit= amt + 1)

    embed = discord.Embed(
    title="Message clear",
    description=f"{amt} messages purged!",
    color=discord.Color.red()
    )
    confirmation = await ctx.send(embed=embed)

    await confirmation.delete(delay=3)

@bot.command()
@commands.has_permissions(kick_members=True)

async def kick(ctx, member: discord.Member, *, reason="no reasons provided"):
    await member.kick(reason=reason)

    embed = discord.Embed(
    title="User kicked",
    description=f"{member} was kicked.",
    color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have to permission to do that!")
    
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Usage: !kick (User) (Reason)")
    

@bot.command()
@commands.has_permissions(ban_members=True)

async def ban(ctx, member: discord.Member, *, reason="no reason provided"):

    await member.ban(reason=reason)

    embed = discord.Embed(
    title="User banned",
    description=f"{member} was banned.",
    color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@ban.error
async def ban_error(ctx, error):

    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You dont have to permission to do that!")
    
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Usage: !ban (User) (Reason)")

@bot.command()
@commands.has_permissions(moderate_members=True)

async def timeout(ctx, member: discord.Member, *, min: int):

    duration= timedelta(minutes=min)

    await member.timeout(duration)

    embed = discord.Embed(
    title="User Timedout",
    description=f"{member} was timedout.",
    color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@timeout.error
async def timeout_error(ctx, error):

    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You dont have to permission to do that!")
    
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Usage: !timeout (User) (Duration)")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def warn(ctx, member: discord.Member, *, reason="reason not given"):
    
    cursor.execute(
    "INSERT INTO warnings (user_id, reason) VALUES (?, ?)",
    (member.id, reason))
    
    conn.commit()

    cursor.execute(
    "SELECT COUNT(*) FROM warnings WHERE user_id = ?",
    (member.id,))
    
    count = cursor.fetchone()[0]

    embed = discord.Embed(
    title="User Warned",
    description=f"{member} was warned because of {reason}\n"
    f"warning counts: {count}",
    color=discord.Color.red()
    )

    await ctx.send(embed=embed)

    if count==3:

        await member.timeout(timedelta(hours=1))
        embed = discord.Embed(
        title="User Timeout",
        description=f"{member} reached 3 warnings and got timed out for 1h!",
        color=discord.Color.red()
    )
        await ctx.send(embed=embed)

    if count==5:

        await member.timeout(timedelta(hours=10))
        embed = discord.Embed(
        title="User Timeout",
        description=f"{member} reached 3 warnings and got timed out for 10h!",
        color=discord.Color.red()
    )
        await ctx.send(embed=embed)

    if count==7:

        await member.timeout(timedelta(hours=24))
        embed = discord.Embed(
        title="User Timeout",
        description=f"{member} reached 3 warnings and got timed out for a day!",
        color=discord.Color.red()
    )
        await ctx.send(embed=embed)

@warn.error
async def warnings_error(ctx, error):

    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You dont have to permission to do that!")
    
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Usage: !warn (User) (Reason)")

@bot.command()
async def warns(ctx, member: discord.Member):
    
    cursor.execute(
    "SELECT COUNT(*) FROM warnings WHERE user_id = ?",
    (member.id,))
    
    count = cursor.fetchone()[0]

    embed = discord.Embed(
    title="Warns:",
    description=f"{member.mention} has {count} warnings",
    color=discord.Color.red()
    )
    await ctx.send(embed=embed)

async def log_action(text):
    channel = bot.get_channel(1509206196500955257)

    await channel.send(text)

@bot.command()
@commands.has_permissions(moderate_members=True)

async def clearwarns(ctx, member: discord.Member):

    cursor.execute(
        "DELETE FROM warnings WHERE user_id = ?",
        (member.id,)
    )

    conn.commit()

    embed = discord.Embed(
    title=f"You poured holy water on them!",
    description=f"Cleared {member.mention} of all of their sins!",
    color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command()
async def reasons(ctx, member: discord.Member):

    cursor.execute(
        "SELECT reason FROM warnings WHERE user_id = ?",
        (member.id,)
    )

    results = cursor.fetchall()

    if not results:
        embed = discord.Embed(
        title="Quite the law-abidding one aren't you~?",
        description=f"{member.mention} have not commited any sin!",
        color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        
        return
    
    reasons = "\n".join(
        f"{i+1}. {row[0]}"
        for i, row in enumerate(results)
    )

    embed = discord.Embed(
    title=f"List of warnings!",
    description=f"{member.mention} sins are:\n{reasons}",
    color=discord.Color.red()
    )
    await ctx.send(embed=embed)

#---------------------------------------------------------------AUTO MODERATION------------------------------------------------------------------------

Filtered = [
    "porn",
    "hentai",
    "rule34",
    "r34",
    "nigger",
    "nigga",
    "nga",
    "whore"
]

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

    if len(user_messages[message.author.id]) >= 5:

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


bot.run(TOKEN)