from discord import app_commands
from discord.ext import commands
import discord 

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Check bot latency"
    )
    async def ping(
        self,
        interaction: discord.Interaction
    ):
        
        await interaction.response.send_message(
            f"Pong! {round(self.bot.latency * 1000)}ms" 
        )
    
    @app_commands.command(
        name="slap",
        description="Slap somebody",
    )
    async def slap(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        embed = discord.Embed(
        title="That's harsh...",
        description=f"{member.mention} was slapped by {interaction.user.mention}",
        color=discord.Color.red())
    
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="kiss",
        description="Kiss somebody",
    )
    async def kiss(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        embed = discord.Embed(
        title="Someone's getting feisty!",
        description=f"{member.mention} was kissed by {interaction.user.mention}",
        color=discord.Color.red())
    
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="marry",
        description="Marry somebody",
    )
    async def marry(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        embed = discord.Embed(
        title="Say hi to the newlyweds!",
        description=f"Congraulations to {member.mention} and {interaction.user.mention} marriage!",
        color=discord.Color.red())
    
        await interaction.response.send_message(embed=embed)

async def setup(bot):
   
    await bot.add_cog(Fun(bot)) 
    print("Fun cog loaded!")