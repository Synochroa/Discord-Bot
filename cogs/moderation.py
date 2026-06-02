from discord import app_commands
from discord.ext import commands
import discord 
from datetime import timedelta

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
        interacton: discord.Interaction,
        amt: int
    ):
        await interacton.channel.purge(limit=amt)
        
        embed = discord.Embed(
            title="Message clear",
            description=f"{amt} messages purged!",
            color=discord.Color.red()
        )
        
        await interacton.response.send_message(
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


async def setup(bot):
   
    await bot.add_cog(Moderation(bot)) 
    print("Moderation cog loaded!")