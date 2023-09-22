import discord
from discord import app_commands
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    # This function will be called when the cog is loaded and ready
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print("SlashAvatar.py - ✅")

    @app_commands.command(name="avatar", description="Sends user's avatar in an embed (sends own avatar if the user is left none).")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member=None):
        if member is None:
            member = interaction.user

        avatar_embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Colour.random())
        avatar_embed.set_image(url=member.avatar)
        avatar_embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar)

        await interaction.response.send_message(embed=avatar_embed)

# This function is required to set up the cog for use
# It will be called when you load the cog in your main bot file
async def setup(client):
    await client.add_cog(Avatar(client))
