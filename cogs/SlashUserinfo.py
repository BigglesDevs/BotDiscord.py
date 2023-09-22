import discord
from discord import app_commands
from discord.ext import commands

class UserInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        # Ensure that the tree is synced
        await self.client.tree.sync()
        print("SlashUserInfo.py - ✅")

    @app_commands.command(name="userinfo", description="Displays information about a user.")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member=None):
        try:
            if member is None:
                member = interaction.user

            # Create an embed with user information
            userinfo_embed = discord.Embed(title=f"{member.name}'s Info", color=discord.Colour.random())
            userinfo_embed.set_thumbnail(url=member.avatar)
            userinfo_embed.add_field(name="Username", value=member.name, inline=True)
            userinfo_embed.add_field(name="Discriminator", value=member.discriminator, inline=True)
            userinfo_embed.add_field(name="User ID", value=member.id, inline=False)
            userinfo_embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
            userinfo_embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
            userinfo_embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar)

            await interaction.response.send_message(embed=userinfo_embed)
        except Exception as e:
            print(f"Error in userinfo command: {e}")
            await interaction.response.send_message("An error occurred while fetching user information.")

# This function is required to set up the cog for use
# It will be called when you load the cog in your main bot file
async def setup(client):
    await client.add_cog(UserInfo(client))
