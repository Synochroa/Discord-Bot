from discord import app_commands
from discord.ext import commands
import discord 
from datetime import timedelta
import sqlite3

conn = sqlite3.connect("warnings.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS warnings (
    user_id INTEGER,
    reason TEXT
)
""")
conn.commit()

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
            name="clear",
            description="Clear amt"
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    
    async def clear(
        self,
        interaction: discord.Interaction,
        amt: int
    ):
        await interaction.channel.purge(limit=amt)
        
        embed = discord.Embed(
            title="Message clear",
            description=f"{amt} messages purged!",
            color=discord.Color.red()
        )
        
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    @app_commands.command(
            name="kick",
            description="Kick @User",
    )
    @app_commands.checks.has_permissions(kick_members=True)
    
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):
    
        await member.kick() 
    
        embed = discord.Embed(
            title="User kicked",
            description=f"{member} was kicked for {reason}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
            name="ban",
            description="Ban @User",
    )
    @app_commands.checks.has_permissions(ban_members=True)
    
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):
    
        await member.ban() 
    
        embed = discord.Embed(
            title="User banned",
            description=f"{member} was banned for {reason}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
            name="mute",
            description="Mute @User",
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    
    

    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: int
    ):
        duration = timedelta(minutes=minutes)
        
        await member.timeout(duration) 
    
        embed = discord.Embed(
            title="User muted",
            description=f"{member} was muted for {minutes}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)


    @app_commands.command(
        name="warn",
        description="Warn @User",
    )
    
    @app_commands.checks.has_permissions(moderate_members=True)
    
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):
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

        await interaction.response.send_message(embed=embed)
        
        if count==3:

            await member.timeout(timedelta(hours=1))
            embed = discord.Embed(
            title="User Timeout",
            description=f"{member} reached 3 warnings and got timed out for 1h!",
            color=discord.Color.red()
            )
            await interaction.response.followup.send(embed=embed)
        
        if count==5:
            await member.timeout(timedelta(hours=10))
            embed = discord.Embed(
            title="User Timeout",
            description=f"{member} reached 3 warnings and got timed out for 10h!",
            color=discord.Color.red()
        )
            await interaction.response.followup.send(embed=embed)
        
        if count==7:

            await member.timeout(timedelta(hours=24))
            embed = discord.Embed(
            title="User Timeout",
            description=f"{member} reached 3 warnings and got timed out for a day!",
            color=discord.Color.red()
        )
            await interaction.response.followup.send(embed=embed)

    @app_commands.command(
        name="warns",
        description="sees @User's warns", 
    )

    async def warns(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        cursor.execute(
        "SELECT COUNT(*) FROM warnings WHERE user_id = ?",
        (member.id,))
    
        count = cursor.fetchone()[0]

        embed = discord.Embed(
        title="Warns:",
        description=f"{member.mention} has {count} warnings",
        color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
            name="clearwarns",
            description="clear @User's warnings",
        )
    @app_commands.checks.has_permissions(moderate_members=True)

    async def clearwarns(
            self,
            interaction: discord.Interaction,
            member: discord.Member
        ):

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
            await interaction.response.send_message(embed=embed)
    
    @app_commands.command(
        name="reasons",
        description="see the list of reasons @user was warned "
    )
    async def reasons(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
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
            await interaction.response.send_message(embed=embed)
        
            return
    
        reason = "\n".join(
            f"{i+1}. {row[0]}"
            for i, row in enumerate(results)
            )

        embed = discord.Embed(
            title=f"List of warnings!",
            description=f"{member.mention} sins are:\n{reason}",
            color=discord.Color.red()
            )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot)) 
    print("Moderation cog loaded!")