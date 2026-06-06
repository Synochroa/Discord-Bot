from discord import app_commands
from discord.ext import commands
import discord 

class HelpView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=60) 
            print("Items:", len(self.children))

        @discord.ui.button(
            label="Moderation",
            style=discord.ButtonStyle.red
        )

        async def moderation_button(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button
            ):
                embed=discord.Embed(
                title="Moderation commands",
                description=
                "/kick\n"
                "/ban\n"
                "/mute\n"
                "/warn\n"
                "/unwarn\n"
                "/clearwarns\n"
                "/reasons\n",
                color=discord.Color.red()
            )

                await interaction.response.edit_message (embed=embed, view=self)

        @discord.ui.button(
        label="Fun",
        style=discord.ButtonStyle.green
    )

        async def fun_button(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button
            ):

            embed= discord.Embed(
            title="Fun commands",
            description=
            "/slap\n"
            "/kiss\n"
            "/marry\n"
            "/bite\n"
            "/hug\n"
            "/pat\n"
            "/ping\n",
            color=discord.Color.green()
            )

            await interaction.response.edit_message(
                    embed=embed,
                    view=self
                    )

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

        embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjJhYzNqZWloamFqNmF2YW02bWExdGN3YXRpeWtoaTNqZHVsczg4aSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Gf3AUz3eBNbTW/giphy.gif")

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

        embed.set_image(url="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdzRsYnkyOXV4eHRqYjA3enp4N2xhNDU5ajc5Nmx5emsyNTBod2FiayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QGc8RgRvMonFm/giphy.gif")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="bite",
        description="Bite somebody",
    )
    async def bite(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        embed = discord.Embed(
            title="Ouch!",
            description=f"{member.mention} was bit by {interaction.user.mention}",
            color=discord.Color.red())

        embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMzMwZWt4d2NjMmc4aWl4YWUzZnZiYXUyaG00cTh4ZWpyNHl2Y2hodSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/lrMUMn9lnpaJDsvP0u/giphy.gif")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="hug",
        description="Hug somebody",
    )
    async def hug(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        embed = discord.Embed(
            title="Awwwww!",
            description=f"{interaction.user.mention} hugged {member.mention}",
            color=discord.Color.red())

        embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTJkYzc2dHFrc2F2aHBlNDR6dDgxdWNnZGVmY2lrMXRwcHp2MDN3MyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3bqtLDeiDtwhq/giphy.gif")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="pat",
        description="pat somebody",
    )
    async def pat(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        embed = discord.Embed(
            title="How sweet!",
            description=f"{interaction.user.mention} gave {member.mention} headpats",
            color=discord.Color.red())

        embed.set_image(url="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExa295NXZrZHk5d2RnbmF6MTl2cnhveWZ4eXo1enZ6eGFzd25pNjFkdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/AomVL3N8lTxiuYtI2I/giphy.gif")

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

    @app_commands.command(
        name="help",
        description="show commands list"
)
    
    async def help(
    self,
    interaction: discord.Interaction
    ):
        
        embed=discord.Embed(
            title="Sparkle help",
            description="Choose a category below",
            color=discord.Color.blurple()
            )

        await interaction.response.send_message(
                embed=embed,
                view=HelpView()
                )

async def setup(bot):
   
    await bot.add_cog(Fun(bot)) 
    print("Fun cog loaded!")