import discord
from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    # This function will be called when the cog is loaded and ready
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print("SlashPing.py - ✅")

    @app_commands.command(name="ping", description="Get the bot's latency.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.client.latency * 1000)  # Calculate bot latency in milliseconds

        ping_embed = discord.Embed(title="Ping Command", color=discord.Colour.random())
        ping_embed.add_field(name="Latency", value=f"{latency}ms")
        ping_embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar)

        await interaction.response.send_message(embed=ping_embed)

# This function is required to set up the cog for use
# It will be called when you load the cog in your main bot file
async def setup(client):
    await client.add_cog(Ping(client))
